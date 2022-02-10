const AjaxCall =(k,v,a,csrf,url)=> {
    $.ajax({
        url: url,
        type:"POST",
        data: {
          'AREA':a,
          'KEY': k,
          'VALUE':v,
           csrfmiddlewaretoken:csrf ,
        },
        dataType: 'json',
        success: function (data) {
            console.log("successful")          
            // location.reload(true);       
        },
		error: function(data) {
                console.log("error")
                console.log(data)
            }
      });
}


const ImageUploadAjax = (file,url,csrf,id,type,subtype) =>{	
    /*
    * Description : Ajax to upload image in project Image
    * Type : image
    * Subtype : secondary or primary
    */
	formdata = new FormData();		
		if (formdata) {
            formdata.append("file", file);
            formdata.append("AREA", 'ProjectImageUpload');
            formdata.append('csrfmiddlewaretoken', csrf);
            formdata.append('project', id);
            formdata.append('type', type);
            formdata.append('subtype', subtype);
			jQuery.ajax({
				url: url,
				type: "POST",
				data: formdata,
				processData: false,
				contentType: false,
				success:function(data){
                    location.reload(true); 
                },
                error: function(data) {
                    console.log("error:ImageUploadAjax")
                    console.log(data)
                }
			});
		}						
	
}

const ProjectResponseFormAjax = (project_id,type,response,csrf,url,user)=> {
    /*
    * Description : Ajax to update Model
    * k : KEY
    * v : VALUE
    * a : AREA
    * FormFileds : id, type, response, project
    */
   
    formdata = new FormData();
    if (formdata) 
    {   
        formdata.append("AREA", "RESPONSE");
        formdata.append("created_by", user);
        formdata.append('project', project_id);
        formdata.append('type', type);
        formdata.append('response', response);
        formdata.append('csrfmiddlewaretoken', csrf);
        $.ajax({
            url: url,
            type: "POST",
            data: formdata,
            processData: false,
            contentType: false,
            success: function (data) {
                console.log("successful:ProjectResponseFormAjax")          
                location.reload(true);       
            },
            error: function(data) {
                    console.log("error:ProjectResponseFormAjax")
                    console.log(data)
                }
        });
    }

}