const showConvergenceTrading = () => {
    let item = document.getElementById('application')
    item.style.display = "none";
    item = document.getElementById('theory')
    item.style.display = "initial";
}

const showPythonApplication = () => {
    let item = document.getElementById('theory')
    item.style.display = "none";
    item = document.getElementById('application')
    item.style.display = "initial";
}