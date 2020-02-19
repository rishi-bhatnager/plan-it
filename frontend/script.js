const LIST = document.querySelector(".list");
const ADDBUTTON = document.querySelector(".add");
const COMPBUTTON = document.querySelector(".compile");
const INPUT = document.querySelector("input");

// Adding a task to the list
function addTask(e) {
    if (INPUT.value.length !== 0) {
        e.preventDefault();
        // Bad code, edit later:
        LIST.innerHTML += `<li class="task"><a class="check" href="#"> ✖ </a>
            <a class="entry" href="#"> ${INPUT.value} </a> | <a class="edit" href="#">Edit</a></li>`;
        INPUT.value = "";
        // Adds listener for the new task
        let checks = LIST.querySelectorAll(".check");
        let items = LIST.querySelectorAll(".edit");
        // Might be possible to optimize this so that no loop is needed:
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
            var el = tasks[i];
            // Clear text of any child elements (Seb's bug fix)
            if (el.firstChild) {
                var child = el.firstChild;
                var texts = [];
                while (child) {
                    if (child.nodeType == 3) {
                        texts.push(child.data);
                        console.log(texts);
                    }
                    child = child.nextSibling;
                }
            }

            var text = texts.join("");
            tableSpaces[a].innerHTML = text;

        } else {
            tableSpaces[a].innerHTML = "";
        }
    }
}

// Show task details
function toggleExpansion(e) {
    e.preventDefault();
    // If there is no child element for the task:
    if (this.children.length == 0) {
        var open = false;
    } else {
        var open = true;
    }
    if (!open) {
        open = true;
        var div = document.createElement("div");
        div.setAttribute("class", "details");
        var p = document.createElement("p");
        var text = document.createTextNode("Yee");
        p.appendChild(text);
        div.appendChild(p);
        this.appendChild(div);
    } else {
        open = false;
        this.querySelector("div").remove();
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
