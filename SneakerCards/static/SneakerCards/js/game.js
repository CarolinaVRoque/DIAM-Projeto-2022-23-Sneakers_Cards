
let newWindow;

const openNewWindow = () => {
  const params = `scrollbars=no,resizable=no,status=no,location=no,toolbar=no,menubar=no`;
  newWindow = window.open('http://localhost:3000', 'SneakerCards Game', params);
};


const winCredits = () => {
    console.log('user')
    openNewWindow()
    newWindow.postMessage({user: 'user'},'SneackerCards');
}