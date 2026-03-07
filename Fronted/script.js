const DEFAULT_API = "https://smart-task-manager-api-g911.onrender.com";

let API = localStorage.getItem("apiBase") || DEFAULT_API;
let token = localStorage.getItem("token") || "";

const $ = (id) => document.getElementById(id);

function setMessage(text, isError = false) {
  const message = $("message");
  message.textContent = text;
  message.classList.toggle("error", isError);
}

function updateAuthStatus() {
  $("authStatus").textContent = token ? "Logged in" : "Not logged in";
}

async function apiRequest(path, options = {}, requiresAuth = false) {
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  if (requiresAuth) {
    if (!token) {
      throw new Error("Please login first.");
    }
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API}${path}`, {
    ...options,
    headers,
  });

  let data;
  try {
    data = await response.json();
  } catch {
    data = {};
  }

  if (!response.ok) {
    throw new Error(data.detail || "Request failed");
  }

  return data;
}

async function register() {
  try {
    const email = $("reg_email").value.trim();
    const password = $("reg_password").value;

    if (!email || !password) {
      throw new Error("Email and password are required.");
    }

    await apiRequest("/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    setMessage("Registration successful. Now login.");
  } catch (err) {
    setMessage(err.message, true);
  }
}

async function login() {
  try {
    const email = $("login_email").value.trim();
    const password = $("login_password").value;

    if (!email || !password) {
      throw new Error("Email and password are required.");
    }

    const data = await apiRequest("/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    token = data.access_token || "";
    localStorage.setItem("token", token);
    updateAuthStatus();

    setMessage("Login successful.");
  } catch (err) {
    setMessage(err.message, true);
  }
}

async function createTask() {
  try {
    const title = $("title").value.trim();
    const priority = $("priority").value || null;
    const deadline = $("deadline").value || null;
    const completed = $("completed").checked;

    if (!title) {
      throw new Error("Task title is required.");
    }

    await apiRequest(
      "/task",
      {
        method: "POST",
        body: JSON.stringify({
          title,
          completed,
          priority,
          deadline,
        }),
      },
      true
    );

    setMessage("Task created successfully.");
    $("title").value = "";
    $("priority").value = "";
    $("deadline").value = "";
    $("completed").checked = false;

    await getTasks();
  } catch (err) {
    setMessage(err.message, true);
  }
}

async function getTasks() {
  try {
    const tasks = await apiRequest("/tasks", {}, true);
    const list = $("taskList");
    list.innerHTML = "";

    if (!tasks.length) {
      list.innerHTML = "<li class='muted'>No tasks found.</li>";
      return;
    }

    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.className = "task-item";
      li.innerHTML = `
        <strong>${task.title}</strong>
        <span>Priority: ${task.priority ?? "none"}</span>
        <span>Deadline: ${task.deadline ?? "none"}</span>
        <span>Status: ${task.completed ? "Completed" : "Pending"}</span>
      `;
      list.appendChild(li);
    });

    setMessage("Tasks loaded.");
  } catch (err) {
    setMessage(err.message, true);
  }
}

function saveApiBase() {
  const value = $("apiBase").value.trim();
  API = value || DEFAULT_API;
  localStorage.setItem("apiBase", API);
  setMessage(`API URL set to: ${API}`);
}

function init() {
  $("apiBase").value = API;
  updateAuthStatus();

  $("saveApiBtn").addEventListener("click", saveApiBase);
  $("registerBtn").addEventListener("click", register);
  $("loginBtn").addEventListener("click", login);
  $("createTaskBtn").addEventListener("click", createTask);
  $("loadTasksBtn").addEventListener("click", getTasks);
}

document.addEventListener("DOMContentLoaded", init);