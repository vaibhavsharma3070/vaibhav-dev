[].forEach.call(document.getElementsByClassName('tags-input'), function (el) {
    let hiddenInput = document.createElement('input'),
        mainInput = document.createElement('input'),
        tags = [];
    //name="tags_of_used_technology" class="form-control" id="id_tags_of_used_technology">
    hiddenInput.setAttribute('type', 'hidden');
	hiddenInput.setAttribute('maxlength', '150');
	hiddenInput.setAttribute('Id', el.getAttribute('hidden_input_id'));
	hiddenInput.setAttribute('name', el.getAttribute('hiden_input_name'));
    //hiddenInput.setAttribute('value', el.getAttribute('val'));

    mainInput.setAttribute('type', 'text');
    mainInput.classList.add('main-input');
    mainInput.addEventListener('input', function () {
        let enteredTags = mainInput.value.split(',');
        if (enteredTags.length > 1) {
            enteredTags.forEach(function (t) {
                let filteredTag = filterTag(t);
                if (filteredTag.length > 0)
                    addTag(filteredTag);
            });
            mainInput.value = '';
        }
    });

    mainInput.addEventListener('keydown', function (e) {
        let keyCode = e.which || e.keyCode;
        if (keyCode === 8 && mainInput.value.length === 0 && tags.length > 0) {
            removeTag(tags.length - 1);
        }
    });

    el.appendChild(mainInput);
    el.appendChild(hiddenInput);
    // split existing value
	 let s = el.getAttribute('val')
	 if (s.length > 1)
	 {
		 let sTags = s.split(',');
		 for (var i = 0; i < sTags.length; i++){
		   addTag(sTags[i]);
		 }
	 }else{
		console.log(el.getAttribute('init_value'));
		addTag(el.getAttribute('init_value')); 
	 }

    function addTag (text) {
        let tag = {
            text: text,
            element: document.createElement('span'),
        };

        tag.element.classList.add('tag');
        tag.element.textContent = tag.text;

        let closeBtn = document.createElement('span');
        closeBtn.classList.add('closetag');
        closeBtn.addEventListener('click', function () {
            removeTag(tags.indexOf(tag));
        });
        tag.element.appendChild(closeBtn);

        tags.push(tag);

        el.insertBefore(tag.element, mainInput);

        refreshTags();
    }

    function removeTag (index) {
        let tag = tags[index];
        tags.splice(index, 1);
        el.removeChild(tag.element);
        refreshTags();
    }

    function refreshTags () {
        let tagsList = [];
        tags.forEach(function (t) {
            tagsList.push(t.text);
        });
        hiddenInput.value = tagsList.join(',');
    }

    function filterTag (tag) {
        //return tag.replace(/[^\w -]/g, '').trim().replace(/\W+/g, '-');
		return toTitleCase(tag);
    }
	//Converts string to Title
	var toTitleCase = function (str) 
	{
		str = str.toLowerCase().split(' ');
		for (var i = 0; i < str.length; i++) {
			str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1);
		}
		return str.join(' ');
	};
});
