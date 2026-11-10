// The practice bookshop's web shop: one script for every page and both versions.
// Practice data only. Text is always written with textContent, never as HTML.
(function () {
  "use strict";

  const KEY = "practice-shop-basket";
  const body = document.body;
  const word = body.dataset.basketWord || "basket";   // v1 "basket", v2 "bag"
  const $ = (sel) => document.querySelector(sel);
  const money = (n) => Number(n).toFixed(2);

  function readBasket() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) { return []; }
  }
  function saveBasket(lines) {
    localStorage.setItem(KEY, JSON.stringify(lines));
    showCount();
  }
  function showCount() {
    const el = $("#basket-count");
    if (el) el.textContent = String(readBasket().reduce((n, l) => n + l.qty, 0));
  }
  async function getJSON(url, options) {
    const res = await fetch(url, options);
    return { status: res.status, data: await res.json() };
  }
  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  // ---- search page ----
  function searchPage() {
    const form = $("#search-form");
    const box = $("#search-box");
    const status = $("#search-status");
    const list = $("#results");
    async function run(q) {
      list.replaceChildren();
      status.textContent = "Searching...";
      const { data } = await getJSON("/api/books?q=" + encodeURIComponent(q));
      if (!data.results.length) {
        status.textContent = "No books match “" + q + "”.";
        return;
      }
      status.textContent = data.results.length + (data.results.length === 1 ? " book found." : " books found.");
      data.results.forEach((b) => {
        const li = el("li", "result");
        const a = el("a", "result-link", b.title);
        a.href = "book.html?id=" + encodeURIComponent(b.id);
        li.append(a, el("span", "result-author", b.author), el("span", "result-price", money(b.price)));
        list.append(li);
      });
    }
    form.addEventListener("submit", (e) => { e.preventDefault(); run(box.value.trim()); });
    const q = new URLSearchParams(location.search).get("q");
    if (q) { box.value = q; run(q); }
  }

  // ---- book page ----
  async function bookPage() {
    const id = new URLSearchParams(location.search).get("id");
    const button = $("#add-button");
    const qty = $("#quantity");
    const status = $("#add-status");
    button.disabled = true;
    const { status: code, data } = await getJSON("/api/books/" + encodeURIComponent(id || ""));
    if (code !== 200) { $("#book-title").textContent = "Book not found"; return; }
    $("#book-title").textContent = data.title;
    $("#book-author").textContent = data.author;
    $("#book-price").textContent = money(data.price);
    button.disabled = false;
    button.addEventListener("click", () => {
      const n = Math.max(1, Math.min(10, parseInt(qty.value, 10) || 1));
      const lines = readBasket();
      const line = lines.find((l) => l.id === data.id);
      if (line) line.qty = Math.min(10, line.qty + n); else lines.push({ id: data.id, qty: n });
      saveBasket(lines);
      status.textContent = "Added to " + word + ".";
    });
  }

  // ---- basket page ----
  async function basketPage() {
    const rows = $("#basket-lines");
    const total = $("#basket-total");
    const empty = $("#basket-empty");
    const place = $("#place-order");
    const placed = $("#order-status");
    async function render() {
      const lines = readBasket();
      rows.replaceChildren();
      empty.hidden = lines.length > 0;
      place.disabled = lines.length === 0;
      total.textContent = lines.length ? "Total: ..." : "";
      if (!lines.length) return;
      const books = await Promise.all(lines.map((l) => getJSON("/api/books/" + encodeURIComponent(l.id))));
      let sum = 0;
      const fresh = lines.map((l, i) => {
        const b = books[i].data;
        const lineTotal = b.price * l.qty;
        sum += lineTotal;
        const tr = el("tr", "basket-line");
        tr.dataset.bookId = l.id;
        const remove = el("button", "remove-button", "Remove");
        remove.type = "button";
        remove.addEventListener("click", () => { saveBasket(readBasket().filter((x) => x.id !== l.id)); render(); });
        const cell = el("td");
        cell.append(remove);
        tr.append(el("td", "line-title", b.title), el("td", "line-qty", String(l.qty)), el("td", "line-total", money(lineTotal)), cell);
        return tr;
      });
      rows.replaceChildren(...fresh);   // a new set of rows every time: old handles go stale
      total.textContent = "Total: " + money(sum);
    }
    place.addEventListener("click", async () => {
      place.disabled = true;
      placed.textContent = "Placing your order...";
      const { status, data } = await getJSON("/api/orders", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ lines: readBasket() }),
      });
      if (status === 201) { saveBasket([]); placed.textContent = "Order " + data.number + " placed."; render(); }
      else { placed.textContent = "Sorry, the order could not be placed."; place.disabled = false; }
    });
    render();
  }

  // ---- order help box ----
  function helpPage() {
    const form = $("#help-form");
    const box = $("#order-box");
    const asked = $("#help-asked");
    const reply = $("#help-reply");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const value = box.value;
      asked.textContent = "You asked about: " + value;
      reply.textContent = "Checking...";
      reply.classList.remove("is-ready");
      const { data } = await getJSON("/api/help?order=" + encodeURIComponent(value));
      reply.textContent = data.reply;
      reply.classList.add("is-ready");
    });
  }

  // ---- orders page ----
  async function ordersPage() {
    const list = $("#order-list");
    const { data } = await getJSON("/api/orders");
    $("#order-count").textContent = data.orders.length + (data.orders.length === 1 ? " order" : " orders");
    data.orders.forEach((o) => list.append(el("li", "order", o.number + ": " + money(o.total))));
  }

  showCount();
  const pages = { search: searchPage, book: bookPage, basket: basketPage, help: helpPage, orders: ordersPage };
  if (pages[body.dataset.page]) pages[body.dataset.page]();
})();
