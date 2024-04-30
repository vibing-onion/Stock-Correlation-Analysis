const para_id = [
    "convergence_trading",
    "idea_of_convergence_trading",
    "real_life_example1",
    "real_life_example2",
    "pre_requisite_of_convergence_trading",
    "important_assumption",
    'why_python',
    'methodology_description'
];

const para_id2 = [
    "convergence_trading",
    "idea_of_convergence_trading",
    "real_life_example",
    "pre_requisite_of_convergence_trading",
    "important_assumption",
    'why_python',
    'methodology_description'
];

const setContent = () => {
    for (let i = 0; i < para_id.length; i++){
        let json_path = "https://vibing-onion.github.io/Stock-Correlation-Analysis/asset/content/" + para_id[i] + ".json";
        console.log(json_path);
        fetch(json_path)
            .then(response => response.json())
            .then(data => {
                console.log(data);

                let title = document.getElementById(para_id[i] + "_h");
                title.innerHTML = data["title"];

                let box = document.getElementById(para_id[i] + "_p")
                for(let j = 0; j < data["content"].length; j++){
                    let sentence = document.createElement('p')
                    sentence.innerHTML = data["content"][j]
                    box.appendChild(sentence)
                    if(j != (data["content"].length - 1)){
                        box.appendChild(document.createElement('br'))
                    }
                }
            })
    }
}

function main(){
    setContent()
    for (let i = 0; i < para_id2.length; i++){
        if (i%2 === 0) {
            let item = document.getElementById(para_id2[i] + "_h");
            item.style.textAlign = 'left';
            console.log(item.id + i)
        }
        else {
            let item = document.getElementById(para_id2[i] + "_h");
            item.style.textAlign = 'right';
            console.log(item.id + i)
        }
    }
    showConvergenceTrading()
}

main()
