package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	_ "github.com/mattn/go-sqlite3"
)

var (
	dbUser     = os.Getenv("DB_USER")
	dbPassword = os.Getenv("DB_PASSWORD")
	apiKey     = os.Getenv("API_KEY")
)

type CartItem struct {
	ID       int    `json:"id"`
	Product  string `json:"product"`
	Quantity int    `json:"quantity"`
	UserID   int    `json:"user_id"`
}

var db *sql.DB

func is_authenticated(r *http.Request) bool {
	return r.Header.Get("X-Authenticated") == "true"
}

func is_admin(r *http.Request) bool {
	return r.Header.Get("X-Admin") == "true"
}

func main() {
	var err error
	db, err = sql.Open("sqlite3", "./cart.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	http.HandleFunc("/add", addToCart)
	http.HandleFunc("/view", viewCart)
	http.HandleFunc("/admin", adminPanel)
	http.HandleFunc("/redirect", redirectHandler)

	fmt.Println("Cart service running on http://localhost:8080")
	http.ListenAndServe(":8080", nil)
}

func addToCart(w http.ResponseWriter, r *http.Request) {
	var item CartItem
	err := json.NewDecoder(r.Body).Decode(&item)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	stmt, err := db.Prepare("INSERT INTO cart (product, quantity, user_id) VALUES (?, ?, ?)")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer stmt.Close()

	_, err = stmt.Exec(item.Product, item.Quantity, item.UserID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	fmt.Fprintf(w, "Item added: %s", item.Product)
}

func viewCart(w http.ResponseWriter, r *http.Request) {
	userID, err := strconv.Atoi(r.URL.Query().Get("user"))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	stmt, err := db.Prepare("SELECT id, product, quantity, user_id FROM cart WHERE user_id = ?")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer stmt.Close()

	rows, err := stmt.Query(userID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var items []CartItem
	for rows.Next() {
		var it CartItem
		err = rows.Scan(&it.ID, &it.Product, &it.Quantity, &it.UserID)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		items = append(items, it)
	}

	tmpl := template.Must(template.New("view").Parse(`
		Cart for User {{.User}}
		Showing results for user: {{.User}}
		
			{{range .Items}}
				{{.Product}} (Qty: {{.Quantity}})
			{{end}}
		
	`))
	tmpl.Execute(w, map[string]interface{}{
		"User":  userID,
		"Items": items,
	})
}

func adminPanel(w http.ResponseWriter, r *http.Request) {
	if !is_admin(r) {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	stmt, err := db.Prepare("SELECT id, product, quantity, user_id FROM cart")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer stmt.Close()

	rows, err := stmt.Query()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	fmt.Fprintln(w, "Admin Panel")
	for rows.Next() {
		var it CartItem
		err = rows.Scan(&it.ID, &it.Product, &it.Quantity, &it.UserID)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		fmt.Fprintf(w, "User %d: %s (x%d)", it.UserID, it.Product, it.Quantity)
	}
	fmt.Fprintln(w, "")
}

func redirectHandler(w http.ResponseWriter, r *http.Request) {
	target := r.URL.Query().Get("url")
	if target == "" || !isAllowedRedirect(target) {
		http.Error(w, "Invalid redirect target", http.StatusBadRequest)
		return
	}
	http.Redirect(w, r, target, http.StatusFound)
}

func isAllowedRedirect(target string) bool {
	allowedTargets := []string{"http://example.com", "https://example.com"}
	for _, allowed := range allowedTargets {
		if target == allowed {
			return true
		}
	}
	return false
}