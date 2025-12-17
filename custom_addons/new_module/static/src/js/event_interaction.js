import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
export class TodoListInteraction extends Interaction {
    static selector = ".todo-list-widget";
    setup() {
        this.todos = [];
        this.inputValue = "";
        this.filter = "all"; // all, active, completed
    }
    async willStart() {
        // Load saved todos from localStorage (or server)
        const saved = localStorage.getItem("todos");
        if (saved) {
            this.todos = JSON.parse(saved);
        }
    }
    get filteredTodos() {
        if (this.filter === "active") {
            return this.todos.filter(t => !t.completed);
        }
        if (this.filter === "completed") {
            return this.todos.filter(t => t.completed);
        }
        return this.todos;
    }
    get remainingCount() {
        return this.todos.filter(t => !t.completed).length;
    }
    dynamicContent = {
        ".todo-input": {
            "t-on-input": (ev) => {
                this.inputValue = ev.target.value;
            },
            "t-on-keydown": (ev) => {
                if (ev.key === "Enter" && this.inputValue.trim()) {
                    this.addTodo();
                }
            },
            "t-att-value": () => this.inputValue,
        },
        ".add-btn": {
            "t-on-click": () => this.addTodo(),
            "t-att-disabled": () => !this.inputValue.trim(),
        },
        ".todo-count": {
            "t-out": () => `${this.remainingCount} items left`,
        },
        ".filter-all": {
            "t-on-click": () => this.setFilter("all"),
            "t-att-class": () => ({ active: this.filter === "all" }),
        },
        ".filter-active": {
            "t-on-click": () => this.setFilter("active"),
            "t-att-class": () => ({ active: this.filter === "active" }),
        },
        ".filter-completed": {
            "t-on-click": () => this.setFilter("completed"),
            "t-att-class": () => ({ active: this.filter === "completed" }),
        },
    };
    start() {
        this.renderTodos();
    }
    addTodo() {
        if (!this.inputValue.trim()) return;

        this.todos.push({
            id: Date.now(),
            text: this.inputValue.trim(),
            completed: false,
        });

        this.inputValue = "";
        this.saveTodos();
        this.renderTodos();
    }
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveTodos();
            this.renderTodos();
        }
    }
    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveTodos();
        this.renderTodos();
    }
    setFilter(filter) {
        this.filter = filter;
        this.renderTodos();
    }
    renderTodos() {
        const container = this.el.querySelector(".todo-items");
        this.removeChildren(container, false);

        this.filteredTodos.forEach(todo => {
            const item = document.createElement("div");
            item.className = `todo-item ${todo.completed ? "completed" : ""}`;
            item.innerHTML = `
                <input type="checkbox" ${todo.completed ? "checked" : ""}>
                <span class="todo-text">${todo.text}</span>
                <button class="delete-btn">×</button>
            `;

            this.addListener(item.querySelector("input"), "change", () => {
                this.toggleTodo(todo.id);
            });

            this.addListener(item.querySelector(".delete-btn"), "click", () => {
                this.deleteTodo(todo.id);
            });

            this.insert(item, container);
        });
    }
    saveTodos() {
        localStorage.setItem("todos", JSON.stringify(this.todos));
    }
    destroy() {
        this.saveTodos();
    }
}
registry.category("public.interactions").add("your_module.key_name", TodoListInteraction);
