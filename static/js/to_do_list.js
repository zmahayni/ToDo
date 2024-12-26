const add_task_button = document.getElementById('add_task');
add_task_button.addEventListener('click', () => {
    location.href = '/add_task';
});
const add_cat_button = document.getElementById('add_cat');
add_cat_button.addEventListener('click', () => {
    location.href = '/add_category';
});
const calendar_button = document.getElementById('Calendar');
calendar_button.addEventListener('click', () =>{
    location.href = '/calendar';
})
const journal_button = document.getElementById('Journal');
journal_button.addEventListener('click', () => {
    location.href = '/journal';
})