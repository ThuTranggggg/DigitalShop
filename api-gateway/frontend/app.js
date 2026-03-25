const state = {
    route: window.location.hash || "#/",
    staff: {
        token: localStorage.getItem("digitalshop.staffToken") || "",
        profile: JSON.parse(localStorage.getItem("digitalshop.staffProfile") || "null"),
        activeType: "laptop",
        overview: null,
    },
    customer: {
        token: localStorage.getItem("digitalshop.customerToken") || "",
        profile: JSON.parse(localStorage.getItem("digitalshop.customerProfile") || "null"),
        activeType: "laptop",
        products: [],
        cart: null,
    },
    miniCartOpen: false,
};

const productConfigs = {
    laptop: [
        ["name", "Tên sản phẩm"],
        ["brand", "Thương hiệu"],
        ["cpu", "CPU"],
        ["ram", "RAM"],
        ["storage", "Bộ nhớ"],
        ["screen", "Màn hình"],
        ["price", "Giá", "number"],
        ["stock", "Tồn kho", "number"],
        ["image_url", "Link ảnh"],
        ["description", "Mô tả", "textarea", "wide"],
    ],
    mobile: [
        ["name", "Tên sản phẩm"],
        ["brand", "Thương hiệu"],
        ["chip", "Chip"],
        ["ram", "RAM"],
        ["storage", "Bộ nhớ"],
        ["battery", "Pin"],
        ["camera", "Camera"],
        ["price", "Giá", "number"],
        ["stock", "Tồn kho", "number"],
        ["image_url", "Link ảnh"],
        ["description", "Mô tả", "textarea", "wide"],
    ],
};

function $(selector) {
    return document.querySelector(selector);
}

function $all(selector) {
    return Array.from(document.querySelectorAll(selector));
}

function setNodeText(selector, value) {
    const node = $(selector);
    if (node) node.textContent = value;
}

function formatCurrency(value) {
    return `${new Intl.NumberFormat("vi-VN", {
        maximumFractionDigits: 0,
    }).format(Number(value || 0))} đ`;
}

function toast(message, type = "success") {
    const container = $("#toast-container");
    const item = document.createElement("div");
    item.className = `toast ${type === "error" ? "error" : ""}`;
    item.textContent = message;
    container.appendChild(item);
    setTimeout(() => item.remove(), 3200);
}

async function apiFetch(url, options = {}) {
    try {
        const bodyLog = options.body ? (typeof options.body === 'string' ? options.body.substring(0, 100) : JSON.stringify(options.body).substring(0, 100)) : "";
        console.log(`[API Request] ${options.method || 'GET'} ${url}`, bodyLog);
        const response = await fetch(url, {
            ...options,
            headers: {
                ...(options.body ? { "Content-Type": "application/json" } : {}),
                ...(options.headers || {}),
            },
        });
        console.log(`[API Response] ${options.method || 'GET'} ${url}: Status ${response.status}`);
        const payload = await response.json().catch(() => ({}));
        console.log(`[API Response] ${options.method || 'GET'} ${url}: Payload:`, payload);
        if (!response.ok || payload.success === false) {
            const errorMsg = payload.message || payload.detail || "Yêu cầu thất bại";
            console.error(`[API Error] ${errorMsg}`);
            throw new Error(errorMsg);
        }
        const result = payload.data || payload;
        console.log(`[API Result] ${options.method || 'GET'} ${url}: Returning:`, result);
        return result;
    } catch (error) {
        console.error(`[Fetch Error] ${url}:`, error.message, error);
        throw error;
    }
}

function persistState() {
    localStorage.setItem("digitalshop.staffToken", state.staff.token || "");
    localStorage.setItem("digitalshop.staffProfile", JSON.stringify(state.staff.profile || null));
    localStorage.setItem("digitalshop.customerToken", state.customer.token || "");
    localStorage.setItem("digitalshop.customerProfile", JSON.stringify(state.customer.profile || null));
}

async function safeLoadAfterLogin(loader, warningMessage) {
    try {
        await loader();
        return true;
    } catch (error) {
        console.error("[Post Login Error]", error.message, error);
        toast(`${warningMessage}: ${error.message}`, "error");
        return false;
    }
}

function clearStaffSession() {
    state.staff.token = "";
    state.staff.profile = null;
    state.staff.overview = null;
}

function clearCustomerSession() {
    state.customer.token = "";
    state.customer.profile = null;
    state.customer.products = [];
    state.customer.cart = null;
    state.miniCartOpen = false;
}

function initials(name = "Khách") {
    return name
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((word) => word[0])
        .join("")
        .toUpperCase() || "KH";
}

function skeletonTemplate(count = 4) {
    return Array.from({ length: count }).map(() => `
        <article class="skeleton-card">
            <div class="skeleton-block skeleton-image"></div>
            <div class="skeleton-block" style="height: 18px;"></div>
            <div class="skeleton-block" style="height: 16px; width: 70%;"></div>
            <div class="skeleton-block" style="height: 16px;"></div>
        </article>
    `).join("");
}

function productBadge(product, type) {
    if (Number(product.stock) <= 5) return "Sắp hết hàng";
    if ((type === "laptop" && Number(product.price) >= 35000000) || (type === "mobile" && Number(product.price) >= 20000000)) {
        return "Bán chạy";
    }
    return "Mới";
}

function productVisual(product) {
    if (product.image_url) {
        return `<img src="${product.image_url}" alt="${product.name}" onerror="this.parentElement.innerHTML='<div class=&quot;product-placeholder&quot;>${product.brand}</div>'">`;
    }
    return `<div class="product-placeholder">${product.brand}</div>`;
}

function buildStaffFields(type) {
    $("#staff-form-fields").innerHTML = productConfigs[type]
        .map(([name, label, inputType = "text", extraClass = ""]) => {
            if (inputType === "textarea") {
                return `<label class="${extraClass}">${label}<textarea name="${name}"></textarea></label>`;
            }
            return `<label class="${extraClass}">${label}<input type="${inputType}" name="${name}"></label>`;
        })
        .join("");
}

function fillStaffForm(type, item = {}) {
    const form = $("#staff-product-form");
    form.elements.type.value = type;
    form.elements.id.value = item.id || "";
    buildStaffFields(type);
    for (const [name] of productConfigs[type]) {
        form.elements[name].value = item[name] ?? "";
    }
}

function resetStaffForm() {
    fillStaffForm(state.staff.activeType);
}

function resolveRoute() {
    const rawRoute = window.location.hash || "#/";
    state.route = ["#/", "#/shop", "#/cart", "#/admin"].includes(rawRoute) ? rawRoute : "#/";
}

function setRoute() {
    resolveRoute();
    const views = {
        "#/": "#landing-view",
        "#/shop": "#shop-view",
        "#/cart": "#cart-view",
        "#/admin": "#admin-view",
    };

    Object.values(views).forEach((selector) => $(selector).classList.add("hidden"));
    $(views[state.route] || "#landing-view").classList.remove("hidden");

    document.body.classList.toggle("admin-mode", state.route === "#/admin");
    updateHeaderStatus();
    updateCustomerStatus();
    updateStaffStatus();
}

function updateHeaderStatus() {
    const header = $("#header-status");
    if (state.staff.token && state.staff.profile) {
        header.textContent = `Nhân viên: ${state.staff.profile.username}`;
        return;
    }
    if (state.customer.token && state.customer.profile) {
        header.textContent = `Khách hàng: ${state.customer.profile.username}`;
        return;
    }
    header.textContent = "Chưa đăng nhập";
}

function updateCustomerStatus() {
    const loggedIn = Boolean(state.customer.token && state.customer.profile);
    $("#customer-auth-panel").classList.toggle("hidden", loggedIn);
    $(".shop-layout").classList.toggle("hidden", !loggedIn || state.route === "#/cart");
    $("#shop-view .dashboard-header").classList.toggle("hidden", !loggedIn);
    const shopOverview = $(".shop-overview-grid");
    if (shopOverview) {
        shopOverview.classList.toggle("hidden", !loggedIn || state.route === "#/cart");
    }
    $("#cart-view").classList.toggle("hidden", state.route !== "#/cart" || !loggedIn);
    setNodeText("#customer-profile-name", loggedIn ? state.customer.profile.full_name : "Khách hàng");
    setNodeText("#customer-welcome-text", loggedIn
        ? `${state.customer.profile.email} | ${state.customer.profile.phone}`
        : "Thông tin tài khoản đăng nhập");
    setNodeText("#customer-profile-meta", loggedIn
        ? `Khách hàng: ${state.customer.profile.username}`
        : "Đăng nhập để mở khóa giỏ hàng.");
    setNodeText("#customer-avatar", initials(loggedIn ? state.customer.profile.full_name : "Khách hàng"));
    $("#customer-register-block").classList.toggle("hidden", loggedIn);
    setNodeText("#customer-active-category", state.customer.activeType === "laptop" ? "Laptop" : "Điện thoại");
    setNodeText("#customer-product-count", String(state.customer.products.length || 0));
    setNodeText("#customer-toolbar-result", `${state.customer.products.length || 0} kết quả`);
}

function updateStaffStatus() {
    const loggedIn = Boolean(state.staff.token && state.staff.profile);
    $("#staff-auth-panel").classList.toggle("hidden", loggedIn);
    $("#admin-view .dashboard-header").classList.toggle("hidden", !loggedIn);
    $(".admin-layout").classList.toggle("hidden", !loggedIn);
    const adminOverview = $(".admin-overview-grid");
    if (adminOverview) adminOverview.classList.toggle("hidden", !loggedIn);
    setNodeText("#staff-profile-name", state.staff.profile?.full_name || "Chưa đăng nhập");
    setNodeText("#staff-active-category", state.staff.activeType === "laptop" ? "Laptop" : "Điện thoại");
}

function updateMiniCartState() {
    $("#mini-cart-drawer").classList.toggle("hidden", !state.miniCartOpen);
}

function openProductModal(product) {
    const specs = state.customer.activeType === "laptop"
        ? [product.cpu, product.ram, product.storage, product.screen]
        : [product.chip, product.ram, product.storage, product.battery, product.camera];

    $("#product-modal-media").innerHTML = productVisual(product);
    $("#product-modal-content").innerHTML = `
        <div class="product-detail-header">
            <div class=\"product-badge\">${productBadge(product, state.customer.activeType)}</div>
            <h2>${product.name}</h2>
            <div class="brand-info">${product.brand}</div>
        </div>
        
        <div class="product-detail-pricing">
            <div class="price-label">Giá bán</div>
            <div class="product-modal-price">${formatCurrency(product.price)}</div>
        </div>

        <div class="product-detail-section">
            <div class="section-label">Mô tả sản phẩm</div>
            <p class="product-description-text">${product.description || "Chưa có mô tả chi tiết."}</p>
        </div>

        <div class="product-detail-section">
            <div class="section-label">Thông số kỹ thuật</div>
            <div class="specs-grid">
                ${specs.filter(Boolean).map((spec) => `<div class="spec-item"><span>${spec}</span></div>`).join("")}
            </div>
        </div>

        <div class="product-detail-section">
            <div class="section-label">Tình trạng hàng hóa</div>
            <div class="stock-info">Tồn kho: <strong>${product.stock} ${state.customer.activeType === "laptop" ? "chiếc" : "chiếc"}</strong></div>
        </div>
    `;
    $("#product-modal").classList.remove("hidden");
}

function closeProductModal() {
    $("#product-modal").classList.add("hidden");
}

function renderStaffTable(products) {
    const table = $("#staff-product-table");
    if (!products.length) {
        table.innerHTML = `<tr><td colspan="6"><div class="empty-state">Chưa có sản phẩm nào.</div></td></tr>`;
        return;
    }

    table.innerHTML = products.map((item) => `
        <tr>
            <td>${item.id}</td>
            <td><strong>${item.name}</strong></td>
            <td>${item.brand}</td>
            <td>${formatCurrency(item.price)}</td>
            <td>${item.stock}</td>
            <td>
                <button class="secondary-button inventory-action" data-edit-id="${item.id}">Sửa</button>
                <button class="inventory-action delete" data-delete-id="${item.id}">Xóa</button>
            </td>
        </tr>
    `).join("");

    table.querySelectorAll("[data-edit-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const product = products.find((item) => String(item.id) === button.dataset.editId);
            if (product) {
                fillStaffForm(state.staff.activeType, product);
                toast(`Đang sửa ${state.staff.activeType} #${product.id}`);
            }
        });
    });

    table.querySelectorAll("[data-delete-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const id = button.dataset.deleteId;
            if (!confirm(`Bạn có chắc chắn muốn xóa ${state.staff.activeType} #${id}?`)) return;
            try {
                await apiFetch(`/api/staff/${state.staff.activeType}s/${id}/`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${state.staff.token}` },
                });
                toast("Đã xóa sản phẩm");
                await fetchStaffOverview();
                resetStaffForm();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });
}

async function fetchStaffOverview() {
    state.staff.overview = await apiFetch("/api/staff/products/overview/", {
        headers: { Authorization: `Bearer ${state.staff.token}` },
    });
    const activeList = state.staff.activeType === "laptop" ? state.staff.overview.laptops : state.staff.overview.mobiles;
    setNodeText("#staff-overview-count", `${state.staff.overview.total_laptops} laptop / ${state.staff.overview.total_mobiles} điện thoại`);
    setNodeText("#staff-summary-total", `${state.staff.overview.total_laptops + state.staff.overview.total_mobiles} sản phẩm`);
    setNodeText("#staff-visible-count", `${activeList.length} mục`);
    setNodeText("#staff-active-category", state.staff.activeType === "laptop" ? "Laptop" : "Điện thoại");
    renderStaffTable(activeList);
}

function renderCatalog(products) {
    const grid = $("#customer-product-grid");
    setNodeText("#customer-product-count", String(products.length || 0));
    setNodeText("#customer-toolbar-result", `${products.length || 0} kết quả`);
    setNodeText("#customer-active-category", state.customer.activeType === "laptop" ? "Laptop" : "Điện thoại");
    if (!products.length) {
        grid.innerHTML = `<div class="empty-state">Không tìm thấy sản phẩm phù hợp.</div>`;
        return;
    }

    grid.innerHTML = products.map((product) => {
        const specs = state.customer.activeType === "laptop"
            ? [product.cpu, product.ram, product.storage, product.screen]
            : [product.chip, product.ram, product.storage, product.camera];
        return `
            <article class="product-card compact-product-card">
                <div class="product-image">
                    <div class="product-placeholder product-list-placeholder">${product.brand}</div>
                </div>
                <div class="product-main">
                    <div class="product-topline compact-topline">
                        <div class="product-title-wrap">
                            <div class="catalog-chip">${product.brand}</div>
                            <h4>${product.name}</h4>
                            <p class="product-subtitle">Tồn kho ${product.stock}</p>
                        </div>
                        <div class="product-price">
                            <div class="product-badge">${productBadge(product, state.customer.activeType)}</div>
                            <strong>${formatCurrency(product.price)}</strong>
                        </div>
                    </div>
                    <p class="product-description">${product.description || "Chưa có mô tả sản phẩm."}</p>
                    <div class="hero-badges">
                        ${specs.filter(Boolean).map((spec) => `<span>${spec}</span>`).join("")}
                    </div>
                </div>
                <div class="product-footer compact-footer">
                    <button class="secondary-button small" data-detail-id="${product.id}">Chi tiết</button>
                    <label class="qty-field">
                        <span>SL</span>
                        <input type="number" min="1" max="${product.stock}" value="1" step="1" inputmode="numeric" data-qty-for="${product.id}">
                    </label>
                    <button class="primary-button small" data-add-id="${product.id}">Thêm</button>
                </div>
            </article>
        `;
    }).join("");

    grid.querySelectorAll("[data-detail-id]").forEach((button) => {
        button.addEventListener("click", () => {
            const product = products.find((item) => String(item.id) === button.dataset.detailId);
            if (product) openProductModal(product);
        });
    });

    grid.querySelectorAll("[data-add-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const productId = Number(button.dataset.addId);
            const quantity = Number(grid.querySelector(`[data-qty-for="${productId}"]`).value || 1);
            try {
                await ensureCart();
                await apiFetch("/api/customers/cart/items/", {
                    method: "POST",
                    headers: { Authorization: `Bearer ${state.customer.token}` },
                    body: JSON.stringify({
                        product_type: state.customer.activeType.toUpperCase(),
                        product_id: productId,
                        quantity,
                    }),
                });
                toast("Đã thêm vào giỏ hàng");
                await fetchCartSummary();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });
}

function renderCart(summary) {
    const summaryNode = $("#customer-cart-summary");
    const itemsNode = $("#customer-cart-items");
    setNodeText("#cart-total-amount", `Tổng giỏ hàng: ${formatCurrency(summary?.total_amount || 0)}`);
    setNodeText("#customer-cart-items-count", `${summary?.total_quantity || 0} sản phẩm`);

    if (!summary || !summary.items?.length) {
        summaryNode.innerHTML = `
            <span class="pill-chip">0 sản phẩm</span>
            <strong>${formatCurrency(0)}</strong>
            <span>Chưa có sản phẩm trong giỏ.</span>
        `;
        itemsNode.innerHTML = `<div class="empty-state">Giỏ hàng đang trống.</div>`;
        updateCartOverview(null);
        return;
    }

    summaryNode.innerHTML = `
        <div class="cart-banner-row">
            <span class="pill-chip">${summary.total_items} dòng sản phẩm</span>
            <span class="pill-chip">Tổng SL: ${summary.total_quantity}</span>
        </div>
        <strong>${formatCurrency(summary.total_amount)}</strong>
        <span>Kiểm tra số lượng từng mặt hàng trước khi đặt mua.</span>
    `;

    itemsNode.innerHTML = summary.items.map((item) => `
        <article class="cart-item">
            <div class="cart-item-title">
                <div>
                    <strong>${item.product_name}</strong>
                    <p class="cart-item-subtitle">Đơn giá ${formatCurrency(item.unit_price)}</p>
                </div>
                <strong>${formatCurrency(item.subtotal)}</strong>
            </div>
            <div class="cart-item-meta">
                <span class="pill-chip">${item.product_type}</span>
                <span class="pill-chip">ID ${item.product_id}</span>
                <span class="pill-chip">SL ${item.quantity}</span>
            </div>
            <div class="cart-item-actions">
                <input type="number" min="1" value="${item.quantity}" data-cart-qty="${item.id}">
                <button class="secondary-button small" data-cart-update="${item.id}">Cập nhật</button>
                <button class="primary-button small danger-button" data-cart-delete="${item.id}">Xóa</button>
            </div>
        </article>
    `).join("");
    updateCartOverview(summary);

    itemsNode.querySelectorAll("[data-cart-update]").forEach((button) => {
        button.addEventListener("click", async () => {
            const id = button.dataset.cartUpdate;
            const quantity = Number(itemsNode.querySelector(`[data-cart-qty="${id}"]`).value || 1);
            try {
                await apiFetch(`/api/customers/cart/items/${id}/`, {
                    method: "PUT",
                    headers: { Authorization: `Bearer ${state.customer.token}` },
                    body: JSON.stringify({ quantity }),
                });
                toast("Đã cập nhật giỏ hàng");
                await fetchCartSummary();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });

    itemsNode.querySelectorAll("[data-cart-delete]").forEach((button) => {
        button.addEventListener("click", async () => {
            const id = button.dataset.cartDelete;
            try {
                await apiFetch(`/api/customers/cart/items/${id}/`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${state.customer.token}` },
                });
                toast("Đã xóa khỏi giỏ hàng");
                await fetchCartSummary();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });
}

function updateCartOverview(summary) {
    setNodeText("#cart-overview-lines", String(summary?.total_items || 0));
    setNodeText("#cart-overview-quantity", String(summary?.total_quantity || 0));
    setNodeText("#cart-overview-total", formatCurrency(summary?.total_amount || 0));
}

async function ensureCart() {
    if (!state.customer.token) {
        throw new Error("Vui lòng đăng nhập khách hàng trước.");
    }
    await apiFetch("/api/customers/cart/", {
        method: "POST",
        headers: { Authorization: `Bearer ${state.customer.token}` },
    });
}

async function fetchCartSummary() {
    if (!state.customer.token) {
        state.customer.cart = null;
        renderCart(null);
        renderCartView(null);
        return;
    }
    try {
        await ensureCart();
        state.customer.cart = await apiFetch("/api/customers/cart/summary/", {
            headers: { Authorization: `Bearer ${state.customer.token}` },
        });
        renderCart(state.customer.cart);
        renderCartView(state.customer.cart);
    } catch (error) {
        toast(error.message, "error");
    }
}

function renderCartView(summary) {
    const itemsNode = $("#cart-view-items");
    const summaryNode = $("#cart-view-summary");
    updateCartOverview(summary);

    if (!summary || !summary.items?.length) {
        itemsNode.innerHTML = `<div class="empty-state">Giỏ hàng đang trống.</div>`;
        summaryNode.innerHTML = `
            <div style="padding:12px; background:var(--surface-soft); border-radius:12px;">
                <p class="section-kicker">Tóm tắt</p>
                <p>Chưa có sản phẩm</p>
            </div>
        `;
        return;
    }

    itemsNode.innerHTML = summary.items.map((item) => `
        <article class="cart-item">
            <div class="cart-item-title">
                <div>
                    <strong>${item.product_name}</strong>
                    <p class="cart-item-subtitle">Đơn giá ${formatCurrency(item.unit_price)}</p>
                </div>
                <strong>${formatCurrency(item.subtotal)}</strong>
            </div>
            <div class="cart-item-meta">
                <span class="pill-chip">${item.product_type}</span>
                <span class="pill-chip">ID ${item.product_id}</span>
            </div>
            <div class="cart-item-actions">
                <input type="number" min="1" max="999" value="${item.quantity}" data-qty-for="${item.id}">
                <button class="secondary-button small" data-update-id="${item.id}">Cập nhật</button>
                <button class="danger-button small" data-delete-id="${item.id}">Xóa</button>
            </div>
        </article>
    `).join("");

    summaryNode.innerHTML = `
        <div style="display:grid;gap:12px;">
            <div>
                <span class="section-kicker">Tổng cộng</span>
                <strong style="font-size:1.4rem;color:var(--brand);">${formatCurrency(summary.total_amount)}</strong>
            </div>
            <div style="display:grid;gap:8px;font-size:0.9rem;">
                <div style="display:flex;justify-content:space-between;">
                    <span>Số mặt hàng:</span>
                    <strong>${summary.total_items} dòng</strong>
                </div>
                <div style="display:flex;justify-content:space-between;">
                    <span>Tổng số lượng:</span>
                    <strong>${summary.total_quantity}</strong>
                </div>
            </div>
        </div>
    `;

    // Setup update/delete actions
    itemsNode.querySelectorAll("[data-update-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const itemId = Number(button.dataset.updateId);
            const quantity = Number(itemsNode.querySelector(`[data-qty-for="${itemId}"]`).value || 1);
            try {
                await apiFetch(`/api/customers/cart/items/${itemId}/`, {
                    method: "PATCH",
                    headers: { Authorization: `Bearer ${state.customer.token}` },
                    body: JSON.stringify({ quantity }),
                });
                toast("Cập nhật giỏ hàng thành công");
                await fetchCartSummary();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });

    itemsNode.querySelectorAll("[data-delete-id]").forEach((button) => {
        button.addEventListener("click", async () => {
            const itemId = Number(button.dataset.deleteId);
            try {
                await apiFetch(`/api/customers/cart/items/${itemId}/`, {
                    method: "DELETE",
                    headers: { Authorization: `Bearer ${state.customer.token}` },
                });
                toast("Xóa sản phẩm khỏi giỏ hàng");
                await fetchCartSummary();
            } catch (error) {
                toast(error.message, "error");
            }
        });
    });
}

function showCatalogSkeleton() {
    $("#catalog-skeleton").innerHTML = skeletonTemplate();
    $("#catalog-skeleton").classList.remove("hidden");
    $("#customer-product-grid").classList.add("hidden");
}

function hideCatalogSkeleton() {
    $("#catalog-skeleton").classList.add("hidden");
    $("#customer-product-grid").classList.remove("hidden");
}

async function fetchCustomerProducts(mode = "list") {
    if (!state.customer.token) {
        $("#customer-product-grid").innerHTML = `<div class="empty-state">Đăng nhập khách hàng để xem danh sách sản phẩm.</div>`;
        hideCatalogSkeleton();
        return;
    }

    showCatalogSkeleton();
    const params = new URLSearchParams();
    const form = $("#customer-search-form");
    if (mode === "search") {
        ["q", "brand", "min_price", "max_price"].forEach((field) => {
            const value = form.elements[field].value.trim();
            if (value) params.set(field, value);
        });
    }

    const endpoint = mode === "search"
        ? `/api/customers/${state.customer.activeType}s/search/?${params.toString()}`
        : `/api/customers/${state.customer.activeType}s/`;

    try {
        state.customer.products = await apiFetch(endpoint, {
            headers: { Authorization: `Bearer ${state.customer.token}` },
        });
        hideCatalogSkeleton();
        renderCatalog(state.customer.products);
    } catch (error) {
        hideCatalogSkeleton();
        toast(error.message, "error");
    }
}

function setupRouter() {
    window.addEventListener("hashchange", setRoute);
    setRoute();
}

function setupTabs() {
    $all("[data-staff-tab]").forEach((button) => {
        button.addEventListener("click", async () => {
            state.staff.activeType = button.dataset.staffTab;
            $all("[data-staff-tab]").forEach((node) => node.classList.toggle("active", node === button));
            setNodeText("#staff-active-category", state.staff.activeType === "laptop" ? "Laptop" : "Điện thoại");
            resetStaffForm();
            if (state.staff.token) await fetchStaffOverview();
        });
    });

    $all("[data-customer-type]").forEach((button) => {
        button.addEventListener("click", async () => {
            state.customer.activeType = button.dataset.customerType;
            $all("[data-customer-type]").forEach((node) => node.classList.toggle("active", node === button));
            setNodeText("#customer-active-category", state.customer.activeType === "laptop" ? "Laptop" : "Điện thoại");
            await fetchCustomerProducts();
        });
    });
}

function setupUIActions() {
    $("#mini-cart-button").addEventListener("click", () => {
        window.location.hash = "#/cart";
    });

    $("#cart-checkout-btn").addEventListener("click", () => {
        toast("Tính năng thanh toán đang được phát triển", "info");
    });

    $("#product-modal-close").addEventListener("click", closeProductModal);
    $("#product-modal").addEventListener("click", (event) => {
        if (event.target.id === "product-modal") closeProductModal();
    });
}

function setupForms() {
    $("#staff-login-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        try {
            console.log("[Login] Staff attempting login:", form.elements.username.value);
            const data = await apiFetch("/api/staff/login/", {
                method: "POST",
                body: JSON.stringify({
                    username: form.elements.username.value,
                    password: form.elements.password.value,
                }),
            });
            console.log("[Login] Staff response data:", data);
            
            if (!data || !data.access) {
                throw new Error("Phản hồi đăng nhập không hợp lệ: Thiếu access token");
            }
            
            clearCustomerSession();
            state.staff.token = data.access;
            state.staff.profile = data.staff;
            console.log("[Login] Staff token set:", !!state.staff.token, "Profile:", state.staff.profile?.username);
            
            persistState();
            updateCustomerStatus();
            updateStaffStatus();
            resetStaffForm();
            window.location.hash = "#/admin";
            toast("Đăng nhập nhân viên thành công");
            await safeLoadAfterLogin(fetchStaffOverview, "Đăng nhập thành công nhưng không tải được danh sách sản phẩm");
        } catch (error) {
            console.error("[Login Error] Staff:", error.message);
            toast(error.message, "error");
        }
    });

    $("#staff-product-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const type = form.elements.type.value;
        const id = form.elements.id.value;
        const payload = {};
        for (const [name] of productConfigs[type]) {
            payload[name] = form.elements[name].value;
        }
        payload.price = Number(payload.price);
        payload.stock = Number(payload.stock);

        try {
            await apiFetch(`/api/staff/${type}s/${id ? `${id}/` : ""}`, {
                method: id ? "PUT" : "POST",
                headers: { Authorization: `Bearer ${state.staff.token}` },
                body: JSON.stringify(payload),
            });
            toast(id ? "Đã cập nhật sản phẩm" : "Đã thêm sản phẩm mới");
            resetStaffForm();
            await fetchStaffOverview();
        } catch (error) {
            toast(error.message, "error");
        }
    });

    $("#staff-form-reset").addEventListener("click", resetStaffForm);

    $("#customer-login-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        try {
            console.log("[Login] Customer attempting login:", form.elements.username.value);
            const data = await apiFetch("/api/customers/login/", {
                method: "POST",
                body: JSON.stringify({
                    username: form.elements.username.value,
                    password: form.elements.password.value,
                }),
            });
            console.log("[Login] Customer response data received:", data);
            
            if (!data || !data.access) {
                console.error("[Login] Missing token - data:", data);
                throw new Error("Phản hồi đăng nhập không hợp lệ: Thiếu access token");
            }
            
            clearStaffSession();
            state.customer.token = data.access;
            state.customer.profile = data.customer;
            console.log("[Login] Customer token set:", !!state.customer.token, "Profile:", state.customer.profile?.username);
            
            persistState();
            updateStaffStatus();
            updateCustomerStatus();
            window.location.hash = "#/shop";
            console.log("[Login] Redirecting to shop view");
            toast("Đăng nhập khách hàng thành công");
            await safeLoadAfterLogin(fetchCustomerProducts, "Đăng nhập thành công nhưng không tải được danh sách sản phẩm");
            await safeLoadAfterLogin(fetchCartSummary, "Đăng nhập thành công nhưng không tải được giỏ hàng");
        } catch (error) {
            console.error("[Login Error] Customer:", error.message, error);
            toast(error.message, "error");
        }
    });

    $("#customer-register-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        try {
            await apiFetch("/api/customers/register/", {
                method: "POST",
                body: JSON.stringify({
                    full_name: form.elements.full_name.value,
                    username: form.elements.username.value,
                    email: form.elements.email.value,
                    phone: form.elements.phone.value,
                    password: form.elements.password.value,
                }),
            });
            form.reset();
            toast("Đã tạo tài khoản thành công");
        } catch (error) {
            toast(error.message, "error");
        }
    });

    $("#customer-search-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        await fetchCustomerProducts("search");
    });

    $("#customer-search-reset").addEventListener("click", async () => {
        $("#customer-search-form").reset();
        await fetchCustomerProducts();
    });

    $("#staff-logout").addEventListener("click", () => {
        clearStaffSession();
        persistState();
        updateStaffStatus();
        setNodeText("#staff-overview-count", "0 sản phẩm");
        setNodeText("#staff-summary-total", "0 sản phẩm");
        setNodeText("#staff-visible-count", "0 mục");
        $("#staff-product-table").innerHTML = `<tr><td colspan="6"><div class="empty-state">Đăng nhập nhân viên để quản lý dữ liệu.</div></td></tr>`;
        window.location.hash = "#/";
        toast("Đã đăng xuất nhân viên");
    });

    $("#customer-logout").addEventListener("click", () => {
        clearCustomerSession();
        persistState();
        updateCustomerStatus();
        renderCart(null);
        $("#customer-product-grid").innerHTML = `<div class="empty-state">Đăng nhập khách hàng để xem danh sách sản phẩm.</div>`;
        setNodeText("#customer-product-count", "0");
        setNodeText("#customer-toolbar-result", "0 kết quả");
        setNodeText("#customer-cart-items-count", "0 sản phẩm");
        window.location.hash = "#/";
        toast("Đã đăng xuất khách hàng");
    });
}

async function bootstrap() {
    buildStaffFields(state.staff.activeType);
    setupRouter();
    setupTabs();
    setupUIActions();
    setupForms();
    updateCustomerStatus();
    updateStaffStatus();
    updateMiniCartState();

    if (state.staff.token) {
        try {
            await fetchStaffOverview();
        } catch (error) {
            toast(error.message, "error");
        }
    } else {
        $("#staff-product-table").innerHTML = `<tr><td colspan="6"><div class="empty-state">Đăng nhập nhân viên để quản lý dữ liệu.</div></td></tr>`;
    }

    if (state.customer.token) {
        try {
            await fetchCustomerProducts();
            await fetchCartSummary();
        } catch (error) {
            toast(error.message, "error");
        }
    } else {
        $("#customer-product-grid").innerHTML = `<div class="empty-state">Đăng nhập khách hàng để xem danh sách sản phẩm.</div>`;
        renderCart(null);
    }
}

bootstrap();
