fetch('static/json/matrix_info.json')
    .then((response) => response.json())
    .then((json) => (matrixInformation = json));

function generateEasyHost() {
    generateHost(1, 3, 3, 1, 3, 7);
}

function generateAverageHost() {
    generateHost(1, 3, 6, 2, 3, 9);
}

function generateHardHost() {
    generateHost(2, 3, 6, 1, 6, 12);
}

function generateHost(svPool, svSide, svMod, srPool, srSide, srMod) {
    securityValue = rollWithMod(svPool, svSide, svMod);
    subsystemAccess = rollWithMod(srPool, srSide, srMod);
    subsystemControl = rollWithMod(srPool, srSide, srMod);
    subsystemIndex = rollWithMod(srPool, srSide, srMod);
    subsystemFiles = rollWithMod(srPool, srSide, srMod);
    subsystemSlave = rollWithMod(srPool, srSide, srMod);

    outputToTable();
}

function outputToTable() {
    $('#securityValue').html(securityValue);
    $('#subsystemAccess').html(subsystemAccess);
    $('#subsystemControl').html(subsystemControl);
    $('#subsystemIndex').html(subsystemIndex);
    $('#subsystemFiles').html(subsystemFiles);
    $('#subsystemSlave').html(subsystemSlave);

    //Reveal the Copy Results Button
    $('#copyResults').removeClass('visually-hidden');
}

function rollWithMod(dicePool, diceSide, modifier) {
    let tmpValue = modifier;

    for (let i = 0; i < dicePool; i++) {
        tmpValue += getRandomRange(1, diceSide);
    }

    return tmpValue;
}

function getRandomRange(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function copyToClipboard() {
    //Get the currently selected security code (Host Color)
    const securityCode = $(
        "input[type='radio'][name='radioSecurityCode']:checked"
    ).val();

    const standardFormat = `${securityCode}-${securityValue}/${subsystemAccess}/${subsystemControl}/${subsystemIndex}/${subsystemFiles}/${subsystemSlave}`;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(standardFormat).then(() => {
            alert('Copied to clipboard');
        });
    } else {
        console.log('Browser Not compatible');
    }
}

function openBasicModal(title) {
    $('#genericModalTitle').html(title);

    const modalBody = $('#genericModalBody');
    modalBody.empty();

    //the content that I am adding to the modal will get added here
    const bodyText = matrixInformation[title].description;

    console.log(bodyText);

    const formatedText = myFormat(bodyText);

    console.log(formatedText);

    modalBody.append(formatedText);

    $('#genericModal').modal('show');
}

function myFormat(inputText) {
    // Replace the \n with double <br>
    return inputText.replace(/(?:\r\n|\r|\n)/g, '<br><br>'); // Update the value of paragraph
}
