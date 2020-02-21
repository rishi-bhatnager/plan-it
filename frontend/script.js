const LIST = document.querySelector(".list");
const ADDBUTTON = document.querySelector(".add");
const COMPBUTTON = document.querySelector(".compile");
const INPUT = document.querySelector("input");

const CATEGORIES = ["Exercise", "Leisure", "Household", "Personal", "Work"];
const CATDESCS = [
    "Physical activity. Ex: Jogging",
    "Scheduled breaks or down time. Ex: Netflix with the wife",
    "Things to get done around the home. Ex: Change the lightbulb",
    "Tasks you need to manage for yourself. Ex: Write diary entry",
    "Things for school or your job. Ex: Work on a web application"];

// Adding a task to the list
function addTask(e) {
    if (INPUT.value.length !== 0) {
        e.preventDefault();
        var task = document.createElement("li");
        task.setAttribute("class", "task");

        var check = document.createElement("a");
        check.setAttribute("class", "check");
        check.setAttribute("href", "#");
        var text1 = document.createTextNode(" ✖ ");
        check.appendChild(text1);

        var entry = document.createElement("a");
        entry.setAttribute("class", "entry");
        var text2 = document.createTextNode(` ${INPUT.value} `);
        entry.appendChild(text2);

        var edit = document.createElement("a");
        edit.setAttribute("class", "edit");
        edit.setAttribute("href", "#");
        var text3 = document.createTextNode("Edit");
        edit.appendChild(text3);

        task.appendChild(check);
        task.appendChild(entry);
        task.appendChild(edit);

        LIST.appendChild(task);

        // LIST.innerHTML += `<li class="task"><a class="check" href="#"> ✖ </a>
        //     <a class="entry" href="#"> ${INPUT.value} </a> | <a class="edit" href="#">Edit</a></li>`;
        // INPUT.value = "";
        // Adds listener for the new task
        let checks = LIST.querySelectorAll(".check");
        let items = LIST.querySelectorAll(".edit");
        // Might be possible to optimize this so that no loop is needed:
        for (let i = 0; i < checks.length; i++) {
            checks[i].addEventListener('click', removeTask, false);
            items[i].addEventListener('click', openDetails, false);
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
function openDetails(e) {
    e.preventDefault();
    // If there is no child element for the task:
    if (this.children.length == 0) {
        var open = false;
    } else {
        var open = true;
    }
    if (!open) {
        open = true;
        this.innerHTML = "";
        var div = document.createElement("div");
        var p = document.createElement("p");
        var text = document.createTextNode("Select a Category:");
        p.appendChild(text);
        div.appendChild(p);
        div.setAttribute("class", "details");
        for (let i = 0; i < CATEGORIES.length; i++) {
            var button = document.createElement("button");
            button.setAttribute("class", "category");
            var text = document.createTextNode(CATEGORIES[i]);
            button.appendChild(text);
            div.appendChild(button);
            button.addEventListener('mouseover', showDesc, false)
            button.addEventListener('mouseout', hideDesc, false)
            button.addEventListener('click', selectCat, false)
        }
        this.appendChild(div);
    }
}

// // Collapse task details
// function collapseTasks(e) {
//     e.preventDefault();
//
// }

var catSelected
function selectCat(e) {
    this.setAttribute("style", "background-color: #ff6557;");
    let siblings = this.parentElement.children;
    for (let i = 0; i < siblings.length; i++) {
        siblings[i].removeAttribute("style");
    }
    this.setAttribute("style", "background-color: #ff6557;");
    catSelected = false;
}

// Show the description of each category
function showDesc(e) {
    e.preventDefault();
    //Check if it's open already
    if (this.parentElement.children.length == CATEGORIES.length + 2) {
        var child = this.parentElement.lastElementChild;
        this.parentElement.removeChild(child);
    }
    // Possible place for optimization:
    // Create array of each child (the buttons)
    var nodes = Array.prototype.slice.call(this.parentElement.children)
    // Go thru each child and create node with the corresponding desc if the
    // button that called matches that index:
    for (let i = 0; i < nodes.length; i++) {
        if (nodes[i] == this) {
            var p = document.createElement("p");
            p.setAttribute("class", "cat-desc")
            var text = document.createTextNode(CATDESCS[i-1]);
            p.appendChild(text);
            this.parentElement.appendChild(p);
        }
    }
}

function hideDesc(e) {
    e.preventDefault();
    if (this.parentElement.children.length == CATEGORIES.length + 2) {
        var child = this.parentElement.lastElementChild;
        this.parentElement.removeChild(child);
    }
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
