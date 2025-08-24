const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2"); // Use mysql2 instead of mysql for parameterized queries
const helmet = require("helmet"); // Add helmet for XSS protection

const app = express();
app.use(bodyParser.json());
app.use(helmet());

const DB_USER = process.env.DB_USER;
const DB_PASS = process.env.DB_PASS;
const API_KEY = process.env.API_KEY;

const db = mysql.createConnection({
  host: "localhost",
  user: DB_USER,
  password: DB_PASS,
  database: "cartdb"
});
db.connect();

const is_authenticated = (req) => req.headers["x-authenticated"] === "true";
const is_admin = (req) => req.headers["x-admin"] === "true";

app.post("/add", (req, res) => {
  if (!is_authenticated(req)) {
    return res.status(401).send("Unauthorized");
  }

  const item = req.body;

  const query = "INSERT INTO cart (product, quantity, user_id) VALUES (?, ?, ?)";
  db.execute(query, [item.product, item.quantity, item.user_id], (err) => {
    if (err) {
      console.error("Error inserting into cart:", err);
      res.status(500).send("Error");
    } else {
      res.send(`Added item: ${item.product}`);
    }
  });
});

app.get("/view", (req, res) => {
  if (!is_authenticated(req)) {
    return res.status(401).send("Unauthorized");
  }

  const userId = req.query.user;

  const query = "SELECT * FROM cart WHERE user_id = ?";
  db.execute(query, [userId], (err, results) => {
    if (err) {
      console.error("DB error:", err);
      return res.status(500).send("DB error");
    }

    let html = `Cart for User ${userId}`;
    results.forEach((item) => {
      html += `${item.product} (Qty: ${item.quantity})`;
    });
    html += "";
    res.send(html);
  });
});

app.get("/admin", (req, res) => {
  if (!is_admin(req)) {
    return res.status(401).send("Unauthorized");
  }

  const query = "SELECT * FROM cart";
  db.execute(query, (err, results) => {
    if (err) {
      console.error("DB error:", err);
      return res.status(500).send("DB error");
    }

    let html = "Admin Panel";
    results.forEach((item) => {
      html += `User ${item.user_id}: ${item.product} x${item.quantity}`;
    });
    html += "";
    res.send(html);
  });
});

app.get("/redirect", (req, res) => {
  const url = req.query.url;
  const allowedUrls = ["http://localhost:3000", "https://example.com"];
  if (allowedUrls.includes(url)) {
    res.redirect(url);
  } else {
    res.status(400).send("Invalid redirect URL");
  }
});

app.listen(3000, () => {
  console.log("Cart service running at http://localhost:3000");
});