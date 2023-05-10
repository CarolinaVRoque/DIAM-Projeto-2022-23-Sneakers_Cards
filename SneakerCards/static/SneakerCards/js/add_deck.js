const gridContainer = document.getElementById('deck-grid-container');
const addItemForm = document.getElementById('add-item-form');
let itemCount = 0;

addItemForm.addEventListener('submit', (event) => {
  event.preventDefault();
  itemCount++;

  const newItem = document.createElement('div');
  newItem.classList.add('deck-grid-item');
  newItem.textContent = `Item ${itemCount}`;

  gridContainer.appendChild(newItem);
  console.log()

  // Submit the form to update the database
  addItemForm.submit();
});
