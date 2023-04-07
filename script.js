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
            success: function(svgData) {
               // Handle success here
               const serializer = new XMLSerializer();
               const svgStr = serializer.serializeToString(svgData);

               // console.log(svgStr);
               // console.log("at least it succeeds eh.");
               $('div.svg').html(function() {
                  return svgStr;
               });
            },
            error: function() {
               // Handle error here
               alert("Error. Please Enter a valid molecule name.");
            }
          });
      });

      // click handler for the add element button
      $('#btnAddElement').click(function() {
         const number = $('#element-number').val();
         const code = $('#element-code').val();
         const name = $('#element-name').val();
         const colour1 = $('#element-colour1').val();
         const colour2 = $('#element-colour2').val();
         const colour3 = $('#element-colour3').val();
         const radius = $('#element-radius').val();

         const form = new FormData();

         form.append("number", number);
         form.append("code", code);
         form.append("name", name);
         form.append("colour1", colour1);
         form.append("colour2", colour2);
         form.append("colour3", colour3);
         form.append("radius", radius);


         $.ajax({
            url: 'addElement',
            type: 'POST',
            data: form,
            contentType: false,
            processData: false,
            success: function() {
               // Handle success here
               alert('Success');
            },
            error: function() {
               // Handle error here
               alert("Error. Please enter valid element data.");
            }
          });
      });
       
  }
);
