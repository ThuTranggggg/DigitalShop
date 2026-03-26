const state = {
    route: location.hash || "#/",
    staff: {
        token: localStorage.getItem("digitalshop.staffToken") || "",
        profile: JSON.parse(localStorage.getItem("digitalshop.staffProfile") || "null"),
        type: "laptop",
        dashboard: null,
        imports: [],
    },
    customer: {
        token: localStorage.getItem("digitalshop.customerToken") || "",
        profile: JSON.parse(localStorage.getItem("digitalshop.customerProfile") || "null"),
        type: "laptop",
        products: [],
        cart: null,
        invoices: [],
        selectedInvoice: null,
    },
};

const routeViews = {
    "#/": "landing-view",
    "#/customer-login": "customer-login-view",
    "#/shop": "shop-view",
    "#/cart": "cart-view",
    "#/checkout": "checkout-view",
    "#/invoices": "invoices-view",
    "#/staff-login": "staff-login-view",
    "#/admin": "admin-view",
};

const customerRoutes = new Set(["#/shop", "#/cart", "#/checkout", "#/invoices"]);
const staffRoutes = new Set(["#/admin"]);

const staffFields = {
    laptop: [
        ["name", "Ten san pham"],
        ["brand", "Thuong hieu"],
        ["cpu", "CPU"],
        ["ram", "RAM"],
        ["storage", "Bo nho"],
        ["screen", "Man hinh"],
        ["price", "Gia", "number"],
        ["stock", "Ton kho", "number"],
        ["image_url", "Link anh"],
        ["status", "Trang thai", "select", ["ACTIVE", "HIDDEN"]],
        ["description", "Mo ta", "textarea"],
    ],
    clothes: [
        ["name", "Ten san pham"],
        ["brand", "Thuong hieu"],
        ["category", "Danh muc"],
        ["size", "Size"],
        ["material", "Chat lieu"],
        ["color", "Mau sac"],
        ["price", "Gia", "number"],
        ["stock", "Ton kho", "number"],
        ["image_url", "Link anh"],
        ["status", "Trang thai", "select", ["ACTIVE", "HIDDEN"]],
        ["description", "Mo ta", "textarea"],
    ],
};

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

function money(value) {
    return `${new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 0 }).format(Number(value || 0))} đ`;
}

function formatDate(value) {
    if (!value) return "Khong ro";
    return new Date(value).toLocaleString("vi-VN");
}

function labelForType(type) {
    return type === "laptop" ? "Laptop" : "Clothes";
}

function requestHeaders(token = "", includeJson = false) {
    return {
        ...(includeJson ? { "Content-Type": "application/json" } : {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
}

async function api(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            ...(options.headers || {}),
        },
    });
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || payload.success === false) {
        throw new Error(payload.message || payload.detail || "Yeu cau that bai");
    }
    return payload.data ?? payload;
}

function toast(message, isError = false) {
    const node = document.createElement("div");
    node.className = `toast${isError ? " error" : ""}`;
    node.textContent = message;
    $("#toast-container").appendChild(node);
    setTimeout(() => node.remove(), 3200);
}

function persistSession() {
    localStorage.setItem("digitalshop.staffToken", state.staff.token || "");
    localStorage.setItem("digitalshop.staffProfile", JSON.stringify(state.staff.profile || null));
    localStorage.setItem("digitalshop.customerToken", state.customer.token || "");
    localStorage.setItem("digitalshop.customerProfile", JSON.stringify(state.customer.profile || null));
}

function clearStaffSession() {
    state.staff.token = "";
    state.staff.profile = null;
    state.staff.dashboard = null;
    state.staff.imports = [];
}

function clearCustomerSession() {
    state.customer.token = "";
    state.customer.profile = null;
    state.customer.products = [];
    state.customer.cart = null;
    state.customer.invoices = [];
    state.customer.selectedInvoice = null;
}

function setBodyTheme(route) {
    const body = document.body;
    body.classList.remove("theme-public", "theme-customer", "theme-staff");
    if (staffRoutes.has(route) || route === "#/staff-login") {
        body.classList.add("theme-staff");
        return;
    }
    if (customerRoutes.has(route) || route === "#/customer-login") {
        body.classList.add("theme-customer");
        return;
    }
    body.classList.add("theme-public");
}

function updateHeaderStatus() {
    const label = $("#header-status-label");
    const value = $("#header-status-value");

    if (state.staff.profile) {
        label.textContent = "Staff portal";
        value.textContent = state.staff.profile.username;
    } else if (state.customer.profile) {
        label.textContent = "Customer area";
        value.textContent = state.customer.profile.username;
    } else {
        label.textContent = "Guest Area";
        value.textContent = "Chua dang nhap";
    }

    $$(".nav-link").forEach((link) => {
        const route = link.dataset.navRoute;
        const active =
            route === state.route ||
            (route === "#/customer-login" && state.route === "#/shop") ||
            (route === "#/staff-login" && state.route === "#/admin");
        link.classList.toggle("active", active);
    });

    $$(".workspace-link").forEach((link) => {
        link.classList.toggle("active", link.dataset.customerRoute === state.route);
    });
}

function showRoute(route) {
    Object.values(routeViews).forEach((viewId) => {
        $(`#${viewId}`).classList.add("hidden");
    });
    const activeView = routeViews[route] || routeViews["#/"];
    $(`#${activeView}`).classList.remove("hidden");
}

function guardRoute(route) {
    if (customerRoutes.has(route) && !state.customer.token) {
        return "#/customer-login";
    }
    if (staffRoutes.has(route) && !state.staff.token) {
        return "#/staff-login";
    }
    if (route === "#/customer-login" && state.customer.token) {
        return "#/shop";
    }
    if (route === "#/staff-login" && state.staff.token) {
        return "#/admin";
    }
    return routeViews[route] ? route : "#/";
}

function productBadge(product, type) {
    if (Number(product.stock) <= 5) return "Sap het";
    if (type === "laptop" && Number(product.price) >= 35000000) return "Premium";
    if (type === "clothes" && Number(product.price) >= 900000) return "Trending";
    return "San co";
}

function productSpecs(product, type) {
    if (type === "laptop") {
        return [product.cpu, product.ram, product.storage, product.screen];
    }
    return [product.category, product.size && `Size ${product.size}`, product.material, product.color];
}

function productImage(product) {
    if (product.image_url) {
        return `<img src="${product.image_url}" alt="${product.name}">`;
    }
    return `<div class="product-placeholder">${product.brand || product.category || "Item"}</div>`;
}

function openProductModal(product) {
    $("#product-modal-media").innerHTML = productImage(product);
    $("#product-modal-content").innerHTML = `
        <div class="product-detail-header">
            <p class="panel-kicker">Chi tiet san pham</p>
            <h3>${product.name}</h3>
            <span class="status-pill">${productBadge(product, state.customer.type)}</span>
        </div>
        <div class="detail-price">${money(product.price)}</div>
        <p class="detail-copy">${product.description || "Chua co mo ta."}</p>
        <div class="detail-spec-grid">
            ${productSpecs(product, state.customer.type)
                .filter(Boolean)
                .map((spec) => `<span>${spec}</span>`)
                .join("")}
        </div>
        <div class="detail-stock">Ton kho hien tai: <strong>${product.stock}</strong></div>
    `;
    $("#product-modal").classList.remove("hidden");
}

function buildStaffForm() {
    const container = $("#staff-form-fields");
    container.innerHTML = staffFields[state.staff.type]
        .map(([name, label, kind = "text", options = []]) => {
            if (kind === "textarea") {
                return `
                    <label>
                        <span>${label}</span>
                        <textarea name="${name}"></textarea>
                    </label>
                `;
            }
            if (kind === "select") {
                return `
                    <label>
                        <span>${label}</span>
                        <select name="${name}">
                            ${options.map((option) => `<option value="${option}">${option}</option>`).join("")}
                        </select>
                    </label>
                `;
            }
            return `
                <label>
                    <span>${label}</span>
                    <input type="${kind}" name="${name}">
                </label>
            `;
        })
        .join("");
}

function fillStaffForm(item = {}) {
    buildStaffForm();
    const form = $("#staff-product-form");
    form.elements.id.value = item.id || "";
    staffFields[state.staff.type].forEach(([name, , kind]) => {
        form.elements[name].value = item[name] ?? (kind === "select" ? "ACTIVE" : "");
    });
    $("#staff-form-title").textContent = item.id
        ? `Dang sua ${labelForType(state.staff.type)} #${item.id}`
        : `Them ${labelForType(state.staff.type)} moi`;
}

function currentStaffProducts() {
    if (!state.staff.dashboard) return [];
    return state.staff.type === "laptop"
        ? state.staff.dashboard.laptops || []
        : state.staff.dashboard.clothes || [];
}

function renderStaffDashboard() {
    const dashboard = state.staff.dashboard;
    if (!dashboard) return;

    $("#staff-profile-line").textContent = `${state.staff.profile.full_name} | ${state.staff.profile.email}`;
    $("#staff-total-products").textContent = dashboard.total_products || 0;
    $("#staff-total-stock").textContent = dashboard.total_stock || 0;
    $("#staff-import-count").textContent = dashboard.recent_import_count || 0;
    $("#staff-active-label").textContent = `Dang quan ly ${labelForType(state.staff.type).toLowerCase()}`;
    $("#staff-table-title").textContent = `Danh sach ${labelForType(state.staff.type)}`;

    const rows = currentStaffProducts();
    const tbody = $("#staff-product-table");
    tbody.innerHTML = rows.length
        ? rows
              .map(
                  (item) => `
                    <tr>
                        <td>${item.id}</td>
                        <td>
                            <strong>${item.name}</strong>
                            <div class="table-subline">${item.description || "Chua co mo ta"}</div>
                        </td>
                        <td>${item.brand || "-"}</td>
                        <td>${money(item.price)}</td>
                        <td>${item.stock}</td>
                        <td><span class="status-pill">${item.status || "ACTIVE"}</span></td>
                        <td class="table-actions">
                            <button class="secondary-button small" data-edit="${item.id}" type="button">Sua</button>
                            <button class="danger-button small" data-delete="${item.id}" type="button">Xoa</button>
                        </td>
                    </tr>
                `
              )
              .join("")
        : `<tr><td colspan="7"><div class="empty-state">Chua co san pham trong danh muc nay.</div></td></tr>`;

    tbody.querySelectorAll("[data-edit]").forEach((button) => {
        button.onclick = () => {
            const item = rows.find((row) => String(row.id) === button.dataset.edit);
            fillStaffForm(item);
        };
    });

    tbody.querySelectorAll("[data-delete]").forEach((button) => {
        button.onclick = async () => {
            if (!confirm("Xac nhan xoa san pham nay?")) return;
            try {
                await api(`/api/staff/${state.staff.type}s/${button.dataset.delete}/`, {
                    method: "DELETE",
                    headers: requestHeaders(state.staff.token),
                });
                toast("Da xoa san pham");
                await loadStaffDashboard();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });

    const history = state.staff.imports.length ? state.staff.imports : dashboard.recent_imports || [];
    $("#staff-import-history").innerHTML = history.length
        ? history
              .map(
                  (item) => `
                    <article class="history-card">
                        <strong>${item.product_name}</strong>
                        <p>${item.product_type} | ID ${item.product_id}</p>
                        <p>+${item.quantity_added} | ${item.stock_before} -> ${item.stock_after}</p>
                        <p>${item.note || "Khong co ghi chu"}</p>
                    </article>
                `
              )
              .join("")
        : `<div class="empty-state">Chua co lich su nhap hang.</div>`;

    fillStaffForm();
}

async function loadStaffDashboard() {
    if (!state.staff.token) return;
    const [dashboard, imports] = await Promise.all([
        api("/api/staff/dashboard/", { headers: requestHeaders(state.staff.token) }),
        api("/api/staff/imports/", { headers: requestHeaders(state.staff.token) }),
    ]);
    state.staff.dashboard = dashboard;
    state.staff.imports = imports;
    renderStaffDashboard();
}

function renderCustomerMiniCart() {
    const cart = state.customer.cart;
    if (!cart || !cart.items?.length) {
        $("#customer-mini-cart").innerHTML = `
            <strong>0 san pham</strong>
            <span>Chua co san pham trong gio hang.</span>
        `;
        return;
    }

    $("#customer-mini-cart").innerHTML = `
        <strong>${cart.total_quantity} san pham</strong>
        <span>${money(cart.total_amount)}</span>
    `;
}

function renderCustomerProducts() {
    const products = state.customer.products || [];
    $("#customer-active-category-label").textContent = labelForType(state.customer.type);
    $("#customer-product-count").textContent = `${products.length} san pham`;
    $("#customer-active-helper").textContent =
        state.customer.type === "laptop"
            ? "Laptop duoc dong bo tu laptop-service."
            : "Clothes duoc dong bo tu clothes-service.";
    $("#customer-profile-line").textContent = state.customer.profile
        ? `${state.customer.profile.full_name} | ${state.customer.profile.email}`
        : "Chua dang nhap";

    const grid = $("#customer-product-grid");
    grid.innerHTML = products.length
        ? products
              .map(
                  (product) => `
                    <article class="product-card">
                        <div class="product-media">${productImage(product)}</div>
                        <div class="product-body">
                            <div class="product-head">
                                <div>
                                    <p class="catalog-chip">${product.brand || labelForType(state.customer.type)}</p>
                                    <h4>${product.name}</h4>
                                </div>
                                <span class="status-pill">${productBadge(product, state.customer.type)}</span>
                            </div>
                            <p class="product-description">${product.description || "Chua co mo ta."}</p>
                            <div class="product-specs">
                                ${productSpecs(product, state.customer.type)
                                    .filter(Boolean)
                                    .map((spec) => `<span>${spec}</span>`)
                                    .join("")}
                            </div>
                            <div class="product-foot">
                                <div>
                                    <strong>${money(product.price)}</strong>
                                    <span>Ton kho ${product.stock}</span>
                                </div>
                                <label class="qty-field">
                                    <span>SL</span>
                                    <input type="number" min="1" max="${product.stock}" value="1" data-qty="${product.id}">
                                </label>
                            </div>
                            <div class="product-actions">
                                <button class="secondary-button" data-detail="${product.id}" type="button">Chi tiet</button>
                                <button class="primary-button" data-add="${product.id}" type="button">Them vao gio</button>
                            </div>
                        </div>
                    </article>
                `
              )
              .join("")
        : `<div class="empty-state">Khong co san pham phu hop.</div>`;

    grid.querySelectorAll("[data-detail]").forEach((button) => {
        button.onclick = () => {
            const product = products.find((item) => String(item.id) === button.dataset.detail);
            openProductModal(product);
        };
    });

    grid.querySelectorAll("[data-add]").forEach((button) => {
        button.onclick = async () => {
            const quantityInput = grid.querySelector(`[data-qty="${button.dataset.add}"]`);
            const quantity = Number(quantityInput?.value || 1);
            try {
                await api("/api/customers/cart/", {
                    method: "POST",
                    headers: requestHeaders(state.customer.token),
                });
                await api("/api/customers/cart/items/", {
                    method: "POST",
                    headers: requestHeaders(state.customer.token, true),
                    body: JSON.stringify({
                        product_type: state.customer.type.toUpperCase(),
                        product_id: Number(button.dataset.add),
                        quantity,
                    }),
                });
                toast("Da them vao gio hang");
                await loadCustomerCart();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });
}

async function loadCustomerProducts(isSearch = false) {
    if (!state.customer.token) return;
    const searchParams = new URLSearchParams();
    const form = $("#customer-search-form");
    if (form && isSearch) {
        ["q", "brand", "min_price", "max_price"].forEach((field) => {
            const value = form.elements[field].value.trim();
            if (value) searchParams.set(field, value);
        });
    }

    const endpoint = isSearch
        ? `/api/customers/${state.customer.type}s/search/?${searchParams.toString()}`
        : `/api/customers/${state.customer.type}s/`;

    state.customer.products = await api(endpoint, {
        headers: requestHeaders(state.customer.token),
    });
    renderCustomerProducts();
}

function renderCustomerCart() {
    renderCustomerMiniCart();

    const cart = state.customer.cart;
    $("#cart-items-heading").textContent = `${cart?.total_quantity || 0} san pham`;
    $("#cart-view-summary").innerHTML =
        cart && cart.items?.length
            ? `
                <p>Tong dong san pham: <strong>${cart.total_items}</strong></p>
                <p>Tong so luong: <strong>${cart.total_quantity}</strong></p>
                <p>Tong tam tinh: <strong>${money(cart.total_amount)}</strong></p>
            `
            : `<div class="empty-state">Gio hang dang trong.</div>`;

    const itemsContainer = $("#cart-view-items");
    itemsContainer.innerHTML =
        cart && cart.items?.length
            ? cart.items
                  .map(
                      (item) => `
                        <article class="cart-item">
                            <div class="cart-item-main">
                                <div>
                                    <strong>${item.product_name}</strong>
                                    <p>${item.product_type} | ID ${item.product_id}</p>
                                </div>
                                <strong>${money(item.subtotal)}</strong>
                            </div>
                            <div class="cart-item-actions">
                                <input type="number" min="0" value="${item.quantity}" data-item-qty="${item.id}">
                                <button class="secondary-button small" data-item-update="${item.id}" type="button">Cap nhat</button>
                                <button class="danger-button small" data-item-delete="${item.id}" type="button">Xoa</button>
                            </div>
                        </article>
                    `
                  )
                  .join("")
            : `<div class="empty-state">Gio hang dang trong.</div>`;

    itemsContainer.querySelectorAll("[data-item-update]").forEach((button) => {
        button.onclick = async () => {
            const quantity = Number(itemsContainer.querySelector(`[data-item-qty="${button.dataset.itemUpdate}"]`).value || 0);
            try {
                await api(`/api/customers/cart/items/${button.dataset.itemUpdate}/`, {
                    method: "PATCH",
                    headers: requestHeaders(state.customer.token, true),
                    body: JSON.stringify({ quantity }),
                });
                toast("Da cap nhat gio hang");
                await loadCustomerCart();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });

    itemsContainer.querySelectorAll("[data-item-delete]").forEach((button) => {
        button.onclick = async () => {
            try {
                await api(`/api/customers/cart/items/${button.dataset.itemDelete}/`, {
                    method: "DELETE",
                    headers: requestHeaders(state.customer.token),
                });
                toast("Da xoa san pham khoi gio");
                await loadCustomerCart();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });

    renderCheckoutSummary();
}

function renderCheckoutSummary() {
    const cart = state.customer.cart;
    $("#checkout-items").innerHTML =
        cart && cart.items?.length
            ? cart.items
                  .map(
                      (item) => `
                        <article class="cart-item compact-cart-item">
                            <div class="cart-item-main">
                                <div>
                                    <strong>${item.product_name}</strong>
                                    <p>${item.product_type} | SL ${item.quantity}</p>
                                </div>
                                <strong>${money(item.subtotal)}</strong>
                            </div>
                        </article>
                    `
                  )
                  .join("")
            : `<div class="empty-state">Gio hang trong. Hay quay lai cua hang.</div>`;

    $("#checkout-total-box").innerHTML =
        cart && cart.items?.length
            ? `
                <p>Tong dong san pham: <strong>${cart.total_items}</strong></p>
                <p>Tong so luong: <strong>${cart.total_quantity}</strong></p>
                <p>Tong thanh toan: <strong>${money(cart.total_amount)}</strong></p>
            `
            : `<p>Chua co du lieu checkout.</p>`;
}

async function loadCustomerCart() {
    if (!state.customer.token) return;
    await api("/api/customers/cart/", {
        method: "POST",
        headers: requestHeaders(state.customer.token),
    });
    state.customer.cart = await api("/api/customers/cart/summary/", {
        headers: requestHeaders(state.customer.token),
    });
    renderCustomerCart();
}

function renderInvoiceDetail() {
    const invoice = state.customer.selectedInvoice;
    const container = $("#invoice-detail");
    if (!invoice) {
        container.innerHTML = `<div class="empty-state">Chon mot hoa don de xem chi tiet.</div>`;
        return;
    }

    container.innerHTML = `
        <div class="invoice-sheet">
            <div class="invoice-head">
                <div>
                    <p class="panel-kicker">Invoice</p>
                    <h3>${invoice.invoice_code}</h3>
                </div>
                <span class="status-pill">${invoice.status}</span>
            </div>
            <p>Ngay tao: ${formatDate(invoice.created_at)}</p>
            <p>Ghi chu: ${invoice.note || "Khong co"}</p>
            <div class="invoice-items">
                ${invoice.items
                    .map(
                        (item) => `
                            <div class="invoice-line">
                                <span>${item.product_name} x ${item.quantity}</span>
                                <strong>${money(item.subtotal)}</strong>
                            </div>
                        `
                    )
                    .join("")}
            </div>
            <div class="invoice-total">
                Tong tien: <strong>${money(invoice.total_amount)}</strong>
            </div>
            ${invoice.status === "PENDING" ? '<button class="danger-button" id="cancel-invoice-btn" type="button">Huy hoa don</button>' : ""}
        </div>
    `;

    if (invoice.status === "PENDING") {
        $("#cancel-invoice-btn").onclick = async () => {
            try {
                state.customer.selectedInvoice = await api(`/api/customers/invoices/${invoice.id}/cancel/`, {
                    method: "POST",
                    headers: requestHeaders(state.customer.token),
                });
                toast("Da huy hoa don");
                await loadCustomerInvoices();
            } catch (error) {
                toast(error.message, true);
            }
        };
    }
}

function renderInvoices() {
    const invoices = state.customer.invoices || [];
    $("#invoice-count").textContent = `${invoices.length} hoa don`;
    $("#invoice-list").innerHTML = invoices.length
        ? invoices
              .map(
                  (invoice) => `
                    <article class="invoice-card ${state.customer.selectedInvoice?.id === invoice.id ? "active" : ""}" data-invoice-id="${invoice.id}">
                        <strong>${invoice.invoice_code}</strong>
                        <p>${formatDate(invoice.created_at)}</p>
                        <p>Trang thai: ${invoice.status}</p>
                        <p>Tong tien: ${money(invoice.total_amount)}</p>
                    </article>
                `
              )
              .join("")
        : `<div class="empty-state">Chua co hoa don nao.</div>`;

    $("#invoice-list").querySelectorAll("[data-invoice-id]").forEach((button) => {
        button.onclick = async () => {
            try {
                state.customer.selectedInvoice = await api(`/api/customers/invoices/${button.dataset.invoiceId}/`, {
                    headers: requestHeaders(state.customer.token),
                });
                renderInvoices();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });

    renderInvoiceDetail();
}

async function loadCustomerInvoices() {
    if (!state.customer.token) return;
    state.customer.invoices = await api("/api/customers/invoices/", {
        headers: requestHeaders(state.customer.token),
    });
    state.customer.selectedInvoice =
        state.customer.invoices.find((invoice) => invoice.id === state.customer.selectedInvoice?.id) ||
        state.customer.invoices[0] ||
        null;
    renderInvoices();
}

async function handleCustomerLogin(event) {
    event.preventDefault();
    const form = event.currentTarget;
    try {
        const result = await api("/api/customers/login/", {
            method: "POST",
            headers: requestHeaders("", true),
            body: JSON.stringify({
                username: form.elements.username.value,
                password: form.elements.password.value,
            }),
        });
        clearStaffSession();
        state.customer.token = result.access;
        state.customer.profile = result.customer;
        persistSession();
        toast("Dang nhap customer thanh cong");
        location.hash = "#/shop";
    } catch (error) {
        toast(error.message, true);
    }
}

async function handleStaffLogin(event) {
    event.preventDefault();
    const form = event.currentTarget;
    try {
        const result = await api("/api/staff/login/", {
            method: "POST",
            headers: requestHeaders("", true),
            body: JSON.stringify({
                username: form.elements.username.value,
                password: form.elements.password.value,
            }),
        });
        clearCustomerSession();
        state.staff.token = result.access;
        state.staff.profile = result.staff;
        persistSession();
        toast("Dang nhap staff thanh cong");
        location.hash = "#/admin";
    } catch (error) {
        toast(error.message, true);
    }
}

function bindStaticEvents() {
    window.addEventListener("hashchange", handleRouteChange);

    $("#customer-login-form").addEventListener("submit", handleCustomerLogin);
    $("#staff-login-form").addEventListener("submit", handleStaffLogin);

    $("#customer-search-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            await loadCustomerProducts(true);
        } catch (error) {
            toast(error.message, true);
        }
    });

    $("#customer-search-reset").onclick = async () => {
        $("#customer-search-form").reset();
        try {
            await loadCustomerProducts();
        } catch (error) {
            toast(error.message, true);
        }
    };

    $("#checkout-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            state.customer.selectedInvoice = await api("/api/customers/checkout/", {
                method: "POST",
                headers: requestHeaders(state.customer.token, true),
                body: JSON.stringify({ note: event.currentTarget.elements.note.value }),
            });
            toast("Checkout thanh cong");
            await Promise.all([loadCustomerCart(), loadCustomerInvoices()]);
            location.hash = "#/invoices";
        } catch (error) {
            toast(error.message, true);
        }
    });

    $("#customer-logout").onclick = () => {
        clearCustomerSession();
        persistSession();
        toast("Da dang xuat customer");
        location.hash = "#/customer-login";
    };

    $("#staff-logout").onclick = () => {
        clearStaffSession();
        persistSession();
        toast("Da dang xuat staff");
        location.hash = "#/staff-login";
    };

    $("#staff-form-reset").onclick = () => fillStaffForm();

    $("#staff-product-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const payload = {};
        staffFields[state.staff.type].forEach(([name, , kind]) => {
            payload[name] = kind === "number" ? Number(form.elements[name].value || 0) : form.elements[name].value;
        });

        const id = form.elements.id.value;
        try {
            await api(`/api/staff/${state.staff.type}s/${id ? `${id}/` : ""}`, {
                method: id ? "PUT" : "POST",
                headers: requestHeaders(state.staff.token, true),
                body: JSON.stringify(payload),
            });
            toast(id ? "Da cap nhat san pham" : "Da them san pham");
            fillStaffForm();
            await loadStaffDashboard();
        } catch (error) {
            toast(error.message, true);
        }
    });

    $("#staff-import-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        try {
            await api("/api/staff/imports/", {
                method: "POST",
                headers: requestHeaders(state.staff.token, true),
                body: JSON.stringify({
                    product_type: form.elements.product_type.value,
                    product_id: Number(form.elements.product_id.value),
                    quantity: Number(form.elements.quantity.value),
                    note: form.elements.note.value,
                }),
            });
            toast("Nhap hang thanh cong");
            form.reset();
            form.elements.product_type.value = "LAPTOP";
            await loadStaffDashboard();
        } catch (error) {
            toast(error.message, true);
        }
    });

    $$("[data-customer-type]").forEach((button) => {
        button.onclick = async () => {
            state.customer.type = button.dataset.customerType;
            $$("[data-customer-type]").forEach((item) => item.classList.toggle("active", item === button));
            try {
                await loadCustomerProducts();
            } catch (error) {
                toast(error.message, true);
            }
        };
    });

    $$("[data-staff-type]").forEach((button) => {
        button.onclick = () => {
            state.staff.type = button.dataset.staffType;
            $$("[data-staff-type]").forEach((item) => item.classList.toggle("active", item === button));
            renderStaffDashboard();
        };
    });

    $("#product-modal-close").onclick = () => $("#product-modal").classList.add("hidden");
    $("#product-modal").onclick = (event) => {
        if (event.target.id === "product-modal") {
            $("#product-modal").classList.add("hidden");
        }
    };
}

async function loadRouteData(route) {
    if (customerRoutes.has(route) && state.customer.token) {
        if (route === "#/shop") {
            await Promise.all([loadCustomerProducts(), loadCustomerCart()]);
        }
        if (route === "#/cart" || route === "#/checkout") {
            await loadCustomerCart();
        }
        if (route === "#/invoices") {
            await Promise.all([loadCustomerCart(), loadCustomerInvoices()]);
        }
    }

    if (staffRoutes.has(route) && state.staff.token) {
        await loadStaffDashboard();
    }
}

async function handleRouteChange() {
    const desiredRoute = guardRoute(location.hash || "#/");
    if (desiredRoute !== (location.hash || "#/")) {
        location.hash = desiredRoute;
        return;
    }

    state.route = desiredRoute;
    setBodyTheme(desiredRoute);
    showRoute(desiredRoute);
    updateHeaderStatus();

    try {
        await loadRouteData(desiredRoute);
    } catch (error) {
        toast(error.message, true);
    }
}

async function boot() {
    buildStaffForm();
    fillStaffForm();
    bindStaticEvents();
    await handleRouteChange();
}

boot();
