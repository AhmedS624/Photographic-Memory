const accordiion = document.getElementsByClassName('contentBx');
for (i=0;i<accordiion.length;i++){
   accordiion[i].addEventListener('click',function(){
      this.classList.toggle('active')
   })
}




function myFunction() {
     var file = document.getElementById('formFileMultiple').files[0];

     var reader  = new FileReader();
     // it's onload event and you forgot (parameters)
     reader.onload = function(e)  {
         var image = document.createElement("img");
         // the result image data
         image.src = e.target.result;
         image.height = 300;
         image.width = 350;
         var location = document.getElementById('targetID');
         location.appendChild(image);
      }
      // you have to declare the file loading
      reader.readAsDataURL(file);
      const element = document.getElementById('display')
      element.remove();
   }

