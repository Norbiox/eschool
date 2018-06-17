var uploadField = document.getElementById("id_file");

uploadField.onchange = function() {
    if(this.files[0].size > 10485760){ // 10MB
       alert("File is too big! Max size: 10MB");
       this.value = "";
    };
};
