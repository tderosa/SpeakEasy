$(document).ready(function(e){

    var currentText = "";

    $("#download").click(function(e){
        e.preventDefault();
        saveTextAsFile();
    });

    // channel = asl
    // binding event = ping
    var pusher = new Pusher('4b8b8ec8b7438706bd80');
    var channel = pusher.subscribe('asl');
    channel.bind('ping', function(data) {
        $("#text").val($("#text").val() + data.message + " \n");
        var elem = $("#text");
        elem.scrollTop = 99999999;
    });

    function saveTextAsFile(){
        var textToWrite = $("#text").val();
        var textFileAsBlob = new Blob([textToWrite], {type:'text/plain'});
        var fileNameToSaveAs;
        if ((fileNameToSaveAs = $("#filename").val()) == "") {
            fileNameToSaveAs = "signscribe.txt";
        }
        else {
            fileNameToSaveAs = fileNameToSaveAs + ".txt";
        }

        var downloadLink = document.createElement("a");
        downloadLink.download = fileNameToSaveAs;
        downloadLink.visible = false;
        if (window.webkitURL != null)
        {
            // Chrome allows the link to be clicked
            // without actually adding it to the DOM.
            downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
        }
        else
        {
            // Firefox requires the link to be added to the DOM
            // before it can be clicked.
            downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
            downloadLink.onclick = destroyClickedElement;
            downloadLink.style.display = "none";
            document.body.appendChild(downloadLink);
        }

        downloadLink.click(function(e){
            e.preventDefault();
            return false;
        });
    }

    function fadeText(string){ 
        hex=255 // Initial color value.
            if(hex>0) { //If color is not black yet
            hex-=11; // increase color darkness
            console.log(document.getElementById("text"))
            document.getElementById("text").style.color="rgb("+hex+","+hex+","+hex+")";

            $("#text").val($("#text").val() + $("#testText").val()  + " \n \n");
            setTimeout($("#text").val(),100); 
            }
            else
            hex=255 //reset hex value
    }

    function clearText() {
        console.log("click")
    }



});