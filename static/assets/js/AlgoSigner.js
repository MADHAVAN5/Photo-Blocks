hljs.initHighlightingOnLoad();
let txParamsJS = {};
let algodClient = {};
let indexerClient = {};

// Helper used with JSON.stringify that replaces Uint8Array data with ascii text for display
function toJsonReplace(key, value) {    
    // Return value immediately if null or undefined
    if(value === undefined || value === null){
        return value;
    }

    // Check for uint8 arrays to get buffer for print
    if(value instanceof Uint8Array || (typeof(value)==='object' && value instanceof Array && value.length > 0 && typeof(value[0]) === 'number')){
        // We have a key that is an address type then use the sdk base 58 method, otherwise use base64
        const addressKeys = ['rcv','snd','to','from','manager','reserve','freeze','clawback','c','f','r','m','asnd','arcv','aclose','fadd'];
        if(key && addressKeys.includes(key)) {
            return algosdk.encodeAddress(value);
        }
        return btoa(value);
    }

    // Check for literal string match on object type to cycle further into the recursive replace
    if(typeof(value) === '[object Object]'){
        return JSON.stringify(value,_toJsonReplace,2);
    } 

    // Return without modification
    return value;
}

function check() {
    let checkCodeElem = document.getElementById('check-code');

    if (typeof AlgoSigner !== 'undefined') {
    checkCodeElem.innerHTML = 'AlgoSigner is installed.';
    } else {
    checkCodeElem.innerHTML = 'AlgoSigner is NOT installed.';
    }
}

function connect() {
    let connectCodeElem = document.getElementById('connect-code');

    AlgoSigner.connect()
    .then((d) => {
    connectCodeElem.innerHTML = JSON.stringify(d, null, 2);
    })
    .catch((e) => {
    console.error(e);
    connectCodeElem.innerHTML = JSON.stringify(e, null, 2);
    })
    .finally(() => {
    hljs.highlightBlock(connectCodeElem);
    });
}

function sdkSetup() {
    let sdkSetupCodeElem = document.getElementById('sdk-setup');

    const algodServer = 'https://testnet-algorand.api.purestake.io/ps2';
    const indexerServer = 'https://testnet-algorand.api.purestake.io/idx2';
    const token = { 'X-API-Key': 'B3SU4KcVKi94Jap2VXkK83xx38bsv95K5UZm2lab' }
    const port = '';

    algodClient = new algosdk.Algodv2(token, algodServer, port);
    indexerClient = new algosdk.Indexer(token, indexerServer, port);

    // Health check
    algodClient.healthCheck().do()
    .then(d => { sdkSetupCodeElem.innerHTML = JSON.stringify(d, null, 2); })
    .catch(e => { sdkSetupCodeElem.innerHTML = JSON.stringify(e, null, 2); })
    .finally(() => {
    hljs.highlightBlock(sdkSetupCodeElem);
    });      
}

function accounts(){
    let accountsCodeElem = document.getElementById('accounts-code');

    AlgoSigner.accounts({
    ledger: 'TestNet'
    })
    .then((d) => {
    accounts = d;
    accountsCodeElem.innerHTML = JSON.stringify(d, null, 2);
    })
    .catch((e) => {
    console.error(e);
    accountsCodeElem.innerHTML = JSON.stringify(d, null, 2);
    })
    .finally(() => {
    hljs.highlightBlock(accountsCodeElem);
    });
}

function status(){
    let statusCodeElem = document.getElementById('status-code');

    algodClient.status().do()
    .then((d) => {
    statusCodeElem.innerHTML = JSON.stringify(d, null, 2);
    })
    .catch((e) => {
    console.error(e);
    statusCodeElem.innerHTML = JSON.stringify(e, null, 2);
    })
    .finally(() => {
    hljs.highlightBlock(statusCodeElem);
    });
}

function assets(){
    let assetsCodeElem = document.getElementById('assets-code');

    const name = document.getElementById('name').value;
    const limit = document.getElementById('limit').value;

    indexerClient.searchForAssets()
    .limit(limit)
    .name(name)
    .do()
    .then((d) => {
    assetsCodeElem.innerHTML = JSON.stringify(d, null, 2);
    })
    .catch((e) => {
    console.error(e);
    assetsCodeElem.innerHTML = JSON.stringify(e, null, 2);
    })
    .finally(() => {
    hljs.highlightBlock(assetsCodeElem);
    });
}