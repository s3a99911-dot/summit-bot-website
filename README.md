const state = {
  user: null,
  overview: null,
  features: [],
  violations: [],
  applications: [],
  logs: [],
  owners: [],
  bankAccount: null,
};

const api = async (path, options = {}) => {
  const response = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json();
};

const renderFeatureList = (items) => {
  const container = document.getElementById("featureList");
  if (!container) return;

  container.innerHTML = items
    .map(
      (feature) => `
        <article class="feature-card glass">
          <div class="feature-icon" style="background:${feature.color}22;color:${feature.color};">${feature.icon}</div>
          <h3>${feature.name}</h3>
          <p>${feature.description}</p>
        </article>
      `
    )
    .join("");
};

const renderViolations = (items) => {
  const tbody = document.getElementById("violationsTable");
  if (!tbody) return;

  tbody.innerHTML = items
    .map(
      (item) => `
        <tr>
          <td>${item.id}</td>
          <td>${item.type}</td>
          <td>${item.reason}</td>
          <td>${item.amount}</td>
          <td>${item.officer}</td>
          <td><span class="badge ${item.is_paid ? "success" : "warning"}">${item.status}</span></td>
          <td>${new Date(item.created_at).toLocaleDateString("ar-SA")}</td>
        </tr>
      `
    )
    .join("");
};

const renderApplications = (items) => {
  const container = document.getElementById("applicationList");
  if (!container) return;

  container.innerHTML = items
    .map(
      (app) => `
        <article class="application-card glass">
          <div class="application-meta" style="background:${app.button_color};">
            <span>${app.icon}</span>
            <strong>${app.title}</strong>
          </div>
          <p>${app.description}</p>
          <div class="question-pill">${app.questions.length} أسئلة</div>
          <button class="btn btn-primary">بدء التقديم</button>
        </article>
      `
    )
    .join("");
};

const renderLogs = (items) => {
  const tbody = document.getElementById("logsTable");
  if (!tbody) return;

  tbody.innerHTML = items
    .map(
      (log) => `
        <tr>
          <td>${log.event_type}</td>
          <td>${log.actor_name || "غير محدد"}</td>
          <td>${log.target_name || "غير محدد"}</td>
          <td>${log.description}</td>
          <td>${log.room_name || "غير محدد"}</td>
          <td>${new Date(log.created_at).toLocaleString("ar-SA")}</td>
        </tr>
      `
    )
    .join("");
};

const populateOverview = (overview) => {
  document.getElementById("heroTitle").innerText = overview.site_name || "بوت القمة";
  document.getElementById("botStatus").innerText = overview.bot_status || "Online";
  document.getElementById("guildMembers").innerText = overview.guild_members || 0;
  document.getElementById("ticketCount").innerText = overview.tickets || 0;
  document.getElementById("operationCount").innerText = overview.operations || 0;
  document.getElementById("violationMetric").innerText = overview.violations || 0;
  document.getElementById("bankMetric").innerText = overview.bank_accounts || 0;
  document.getElementById("applicationMetric").innerText = overview.applications || 0;
  document.getElementById("logsMetric").innerText = overview.logs || 0;
};

const renderBankAccount = (account) => {
  if (!account) return;
  document.getElementById("userAvatar").innerText = "U";
  document.getElementById("accountName").innerText = account.name || "اسم صاحب الحساب";
  document.getElementById("accountNumber").innerText = account.number || "#0000";
  document.getElementById("balanceValue").innerText = `${account.balance || 0} SR`;
  document.getElementById("totalDeposit").innerText = account.total_deposit || 0;
  document.getElementById("totalTransfers").innerText = account.total_transfers || 0;
  document.getElementById("loanCount").innerText = account.loan_count || 0;
};

const loadDashboard = async () => {
  try {
    const overview = await api("/overview");
    state.overview = overview;
    populateOverview(overview);

    const features = await api("/features");
    state.features = features;
    renderFeatureList(features);

    const violations = await api("/violations?discord_id=100000000000000001");
    state.violations = violations;
    renderViolations(violations);

    const bank = await api("/bank/100000000000000001");
    state.bankAccount = bank.account;
    renderBankAccount({
      ...bank.account,
      loan_count: 2,
    });

    const applications = await api("/applications");
    state.applications = applications;
    renderApplications(applications);

    const logs = await api("/logs?window=7d");
    state.logs = logs;
    renderLogs(logs);

    const owners = await api("/owners");
    state.owners = owners;
    document.getElementById("ownerCount").innerText = owners.length;
    document.getElementById("ownerMembers").innerText = state.overview.guild_members || 0;
    document.getElementById("ownerViolations").innerText = state.overview.violations || 0;
    document.getElementById("ownerBankCount").innerText = state.overview.bank_accounts || 0;
    document.getElementById("ownerApplications").innerText = state.overview.applications || 0;
    document.getElementById("ownerOperations").innerText = state.overview.operations || 0;
  } catch (error) {
    console.error(error);
  }
};

const bindFilters = () => {
  document.querySelectorAll(".chip").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".chip").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");

      const filter = button.dataset.filter;
      if (filter === "all") {
        renderViolations(state.violations);
        return;
      }

      const filtered = state.violations.filter((v) => {
        if (filter === "paid") return v.is_paid;
        if (filter === "unpaid") return !v.is_paid;
        return true;
      });
      renderViolations(filtered);
    });
  });
};

const bindLogControls = () => {
  document.getElementById("logRange").addEventListener("change", async (event) => {
    const value = event.target.value;
    const logs = await api(`/logs?window=${value}`);
    renderLogs(logs);
  });

  document.getElementById("logSearch").addEventListener("input", (event) => {
    const query = event.target.value.trim().toLowerCase();
    if (!query) {
      renderLogs(state.logs);
      return;
    }

    const filtered = state.logs.filter((log) => {
      const text = `${log.actor_name || ""} ${log.actor_discord_id || ""} ${log.target_name || ""} ${log.event_type || ""}`.toLowerCase();
      return text.includes(query);
    });
    renderLogs(filtered);
  });
};

const saveTheme = async () => {
  const payload = {
    primary_color: document.getElementById("primaryColor").value,
    background_color: document.getElementById("backgroundColor").value,
    button_color: document.getElementById("buttonColor").value,
    card_color: document.getElementById("cardColor").value,
  };

  await api("/settings/theme", {
    method: "POST",
    body: JSON.stringify(payload),
  });
};

const saveOwner = async () => {
  const payload = {
    discord_id: document.getElementById("ownerDiscordId").value,
    username: document.getElementById("ownerUsername").value,
  };

  await api("/owners", {
    method: "POST",
    body: JSON.stringify(payload),
  });
};

const bindActions = () => {
  document.getElementById("discordLoginBtn").addEventListener("click", async () => {
    const response = await api("/auth/callback?code=demo-auth");
    state.user = response;
    alert(`تم تسجيل الدخول بنجاح كـ ${response.username}`);
  });

  document.getElementById("ownerPanelBtn").addEventListener("click", () => {
    document.getElementById("ownerPanelSection").classList.toggle("hidden");
  });

  document.getElementById("saveThemeBtn").addEventListener("click", saveTheme);
  document.getElementById("saveOwnerBtn").addEventListener("click", saveOwner);
};

window.addEventListener("DOMContentLoaded", async () => {
  await loadDashboard();
  bindFilters();
  bindLogControls();
  bindActions();
});
