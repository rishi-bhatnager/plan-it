const LIST = document.querySelector(".list");
const BUTTON = document.querySelector("button");
const INPUT = document.querySelector("input");

// Adding a task to the list
function addTask(e) {
    e.preventDefault();
    LIST.innerHTML += `<li class="task"><a class="check" href="#"> ◦ </a><a class="entry" href="#"> ${INPUT.value} </a></li>`;
    INPUT.value = "";
    // Add listener for the new task
    let tasks = LIST.querySelectorAll(".check");
    for (i = 0; i < tasks.length; i++) {
        tasks[i].addEventListener('click', removeTask, false);
    }
}

// Remove task from list
function removeTask(e) {
    e.preventDefault();
    console.log(e.target);
    this.parentElement.remove();
}

// Listen for enter pressed
INPUT.addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode === 13) {
        BUTTON.click();
    }
}, false);

// Listen for button click
BUTTON.addEventListener("click", addTask, false);
