const LIST = document.querySelector(".list");
const ADDBUTTON = document.querySelector(".add");
const COMPBUTTON = document.querySelector(".compile");
const INPUT = document.querySelector("input");

// Adding a task to the list
function addTask(e) {
    if (INPUT.value.length !== 0) {
        e.preventDefault();
        LIST.innerHTML += `<li class="task"><a class="check" href="#"> ✖ </a><a class="entry" href="#"> ${INPUT.value} </a></li>`;
        INPUT.value = "";
        // Add listener for the new task
        let checks = LIST.querySelectorAll(".check");
        let items = LIST.querySelectorAll(".entry");
        for (i = 0; i < checks.length; i++) {
            checks[i].addEventListener('click', removeTask, false);
            items[i].addEventListener('click', toggleExpansion, false);
        }
    }
}

// Remove task from list
function removeTask(e) {
    e.preventDefault();
    this.parentElement.remove();
}

// Compile the Schedule
function compileList() {
    let tasks = document.querySelectorAll(".entry");
    let tableSpaces = document.querySelectorAll("td");
    for (let i = 0; i < (tableSpaces.length / 2); i++) {
        let a = 2 * i + 1;
        if (i < tasks.length) {
            tableSpaces[a].innerHTML = tasks[i].innerHTML;
        } else {
            tableSpaces[a].innerHTML = "";
        }
    }
}

// Show task details
function toggleExpansion(e) {
    e.preventDefault();
    if (this.children.length == 0) {
        var open = false;
    } else {
        var open = true;
    }
    if (!open) {
        open = true;
        var para = document.createElement("p");
        var node = document.createTextNode("Details...");
        para.appendChild(node);
        this.appendChild(para);
    } else {
        open = false;
        this.querySelector("p").remove();
    }
}

// Collapse task details
function collapseTasks(e) {
    e.preventDefault();

}


// Listen for enter pressed
INPUT.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        ADDBUTTON.click();
    }
}, false);

// Listen for button clicks
ADDBUTTON.addEventListener("click", addTask, false);
COMPBUTTON.addEventListener("click", compileList, false);
