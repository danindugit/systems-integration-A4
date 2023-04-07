/* javascript to accompany jquery.html */

$(document).ready(
   /* this defines a function that gets called after the document is in memory */
  function()
  {
      // click handler for uploadSDF button
      $('#btnInsMol').click(function() {      
         // post request
         const fileName = $('#fileSdf')[0].files[0]
         const molName= $('#formMolName').val()

         const form = new FormData();

         form.append("fileInfo", fileName)
         form.append("mol", molName)

         $.ajax({
            url: 'uploadSDF',
            type: 'POST',
            data: form,
            contentType: false,
            processData: false,
            success: function() {
              // Handle success here
              alert("Molecule Successfully Added.");
            },
            error: function() {
              // Handle error here
              alert("Error. Please Enter a valid sdf file and molecule name.");
            }
          });
       });

      // click handler for the display molecule button
      $('#btnDisplay').click(function() {
         const molName = $('#displayMolName').val();

         const form = new FormData();

         form.append("mol", molName);

         $.ajax({
            url: 'display',
            type: 'POST',
            data: form,
            contentType: false,
            processData: false,
            success: function(svgstr) {
               // Handle success here
               $('#svgMol').html(function(){
                  return svgstr;
               });
            },
            error: function() {
               // Handle error here
               alert("Error. Please Enter a valid molecule name.");
            }
          });
      });
       
  }
);