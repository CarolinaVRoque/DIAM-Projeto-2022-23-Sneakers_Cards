const gridContainer = document.getElementById('deck-grid-container');
const addItemBtn = document.getElementById('add-item-btn');
let itemCount = 0;

addItemBtn.addEventListener('click', () => {
  itemCount++;

  const newItem = document.createElement('div');
  newItem.classList.add('deck-grid-item');

  const link = document.createElement('a');
  link.href = 'https://example.com';  // Replace with your desired link URL

  const image = document.createElement('img');
  image.src = `SneakerCards/static/SneakerCards/images/background.png`;  // Replace with your image path and extension
  image.alt = `Item ${itemCount}`;  // Replace with appropriate alt text

  link.appendChild(image);
  newItem.appendChild(link);

  gridContainer.appendChild(newItem);
});
