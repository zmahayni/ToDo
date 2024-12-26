const home_button = document.getElementById("Home");
home_button.addEventListener('click', () => {
    location.href = '/'
})
const calendar_button =  document.getElementById("Calendar");
calendar_button.addEventListener('click', () => {
    location.href = '/calendar'
})
const note = document.getElementById("notes")
const save_button = document.getElementById("Save")

async function saveNotes(notes){
    const response = await fetch("/save_notes", {
        method: "POST",
        headers: {"Content-type": "application/json"},
        body: JSON.stringify({notes})
    })
    const result = await response.json();
    if(result.status === "success") {
        location.href = '/journal'
    } else {
        alert("Failed to save notes: " + result.message);
    }
}

save_button.addEventListener('click', () => {
    saveNotes(note.innerHTML.trim());
})
