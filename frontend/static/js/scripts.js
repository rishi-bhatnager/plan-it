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
        let task = document.createElement("li");
        task.setAttribute("class", "task");

        let check = document.createElement("a");
        check.setAttribute("class", "check");
        check.setAttribute("href", "#");
        let text1 = document.createTextNode(" ✖ ");
        check.appendChild(text1);

        let entry = document.createElement("a");
        entry.setAttribute("class", "entry");
        let text2 = document.createTextNode(` ${INPUT.value} `);
        entry.appendChild(text2);

        let edit = document.createElement("a");
        edit.setAttribute("class", "edit");
        edit.setAttribute("href", "#");
        let text3 = document.createTextNode("Edit");
        edit.appendChild(text3);

        task.appendChild(check);
        task.appendChild(entry);
        task.appendChild(edit);

        LIST.appendChild(task);

        INPUT.value = "";

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
        let div = document.createElement("div");
        let p = document.createElement("p");
        let text = document.createTextNode("Select a Category:");
        p.appendChild(text);
        div.appendChild(p);
        div.setAttribute("class", "details");
        for (let i = 0; i < CATEGORIES.length; i++) {
            let button = document.createElement("button");
            button.setAttribute("class", "category");
            let text = document.createTextNode(CATEGORIES[i]);
            button.appendChild(text);
            div.appendChild(button);
            button.addEventListener('mouseover', showDesc, false)
            button.addEventListener('mouseout', hideDesc, false)
            button.addEventListener('click', selectCat, false)
        }
        let p2 = document.createElement("p");
        let text2 = document.createTextNode("How long do you expect this to take?");
        p2.appendChild(text2);

        let inputdiv = document.createElement("div");

        let input = document.createElement("input");
        input.setAttribute("style", "width: 120px;");
        input.setAttribute("placeholder", "Enter time");

        // Check for input submission
        input.addEventListener("keyup", function(event) {
            event.preventDefault();
            if (event.keyCode === 13) {
                if (isNaN(input.value - 1)) {
                    console.log("u fool!");
                }
            }
        }, false);

        let hours = document.createTextNode(" Hours ");

        let p3 = document.createElement("p");
        let text3 = document.createTextNode("When does it need to be done by?")
        p3.appendChild(text3);

        let slider = document.createElement("input");
        slider.setAttribute("type","range");
        slider.setAttribute("min", "1");
        slider.setAttribute("max", "100");
        slider.setAttribute("value", "0");
        slider.setAttribute("class", "slider");

        let p4 = document.createElement("p");
        let text4 = document.createTextNode(slider.value);
        p4.appendChild(text4);

        inputdiv.appendChild(input);
        inputdiv.appendChild(hours);
        div.appendChild(p2);
        div.appendChild(inputdiv);
        div.appendChild(p3)
        div.appendChild(slider);
        div.appendChild(p4);
        this.appendChild(div);
    }
}

// // Collapse task details
// function collapseTasks(e) {
//     e.preventDefault();
//
// }

function selectCat(e) {
    this.setAttribute("style", "background-color: #ff6557;");
    let siblings = this.parentElement.children;
    for (let i = 0; i < siblings.length; i++) {
        siblings[i].removeAttribute("style");
    }
    this.setAttribute("style", "background-color: #ff6557;");
}

// Show the description of each category
function showDesc(e) {
    e.preventDefault();
    //Check if it's open already
    if (this.parentElement.children.length == CATEGORIES.length + 7) {
        var child = this.parentElement.children[6];
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
            this.parentElement.insertBefore(p, this.parentElement.children[6]);
        }
    }
}

function hideDesc(e) {
    e.preventDefault();
    if (this.parentElement.children.length == CATEGORIES.length + 7) {
        var child = this.parentElement.children[6];
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
