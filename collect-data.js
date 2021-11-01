const axios = require("axios");
const fs = require("fs");

const session_url = "https://api.challonge.com/v1/tournaments/";
let promises = [];

for (var i = 1; i <= 50; i++){
    console.log(i)
    promises.push(axios.get(session_url+`pinkmelee${i}/participants.json`,{
        params:{
            api_key: "BTMogGUKn1MlV6oUnr4foEuBgPoAIBctQBJAPYVE"
        }
    }))

    promises.push(axios.get(session_url+`pinkmelee${i}/matches.json`,{
        params:{
            api_key: "BTMogGUKn1MlV6oUnr4foEuBgPoAIBctQBJAPYVE"
        }
    }))
}

Promise.all(promises).then(responses => {
    for (var i = 0; i < responses.length; i++){
        console.log();
        const path = responses[i].request.path.split('/');
        const tourney = path[3];
        const type = path[4].split("?")[0];
        const data = responses[i].data;
        fs.mkdir(`./tourney/${tourney}`, {recursive:true}, ()=>{
            fs.writeFile(`./tourney/${tourney}/${tourney + "-" + type}`, JSON.stringify(data), {}, ()=>{})
        });
        console.log(tourney, type)
    }
});