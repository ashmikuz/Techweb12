
function drawmarkers(checkbox)
{
	if(checkbox.checked)
		{
			aggrurl=getaggr(checkbox.id);
			prova=document.getElementById("prova");
			prova.appendChild(document.createTextNode("ammaccabanane"));
		}
}

