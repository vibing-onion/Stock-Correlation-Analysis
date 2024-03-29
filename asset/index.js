const para_id = [
    "convergence_trading",
    "idea_of_convergence_trading",
    "real_life_example",
    "pre_requisite_of_convergence_trading",
    "important_assumption"
];

async function fetch_json(json_path){
    try{

    }
    catch(error){
        console.log(error);
    }
}

async function main(){
    for (let i = 0; i < para_id.length; i++){
        //let box = document.getElementById(para_id[i]);
        let json_path = "./content/" + para_id[i] + ".json";

        const content = (await fetch(json_path)).json();
        console.log(content)

    //box.value = 
    }
}

main()