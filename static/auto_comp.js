document.addEventListener('DOMContentLoaded', function () {
    function autocomplete(inp, arr) {
        var currentFocus;

        inp.addEventListener("input", function (e) {
            var a, b, i, val = this.value;
            closeAllLists();
            if (!val) { return false; }
            currentFocus = -1;
            a = document.createElement("DIV");
            a.setAttribute("id", this.id + "autocomplete-list");
            a.setAttribute("class", "autocomplete-items form-control");
            this.parentNode.appendChild(a);
            for (i = 0; i < arr.length; i++) {
                if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                    b = document.createElement("DIV");
                    b.setAttribute("role", "button")
                    b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
                    b.innerHTML += arr[i].substr(val.length);
                    b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
                    b.addEventListener("click", function (e) {
                        inp.value = this.getElementsByTagName("input")[0].value;
                        closeAllLists();
                    });
                    a.appendChild(b);
                }
            }
        });
        inp.addEventListener("keydown", function (e) {
            var x = document.getElementById(this.id + "autocomplete-list");
            if (x) x = x.getElementsByTagName("div");
            if (e.keyCode == 40) {
                currentFocus++;
                addActive(x);
            } else if (e.keyCode == 38) {
                currentFocus--;
                addActive(x);
            } else if (e.keyCode == 13) {
                e.preventDefault();
                if (currentFocus > -1) {
                    if (x) x[currentFocus].click();
                }
            }
        });
        function addActive(x) {
            if (!x) return false;
            removeActive(x);
            if (currentFocus >= x.length) currentFocus = 0;
            if (currentFocus < 0) currentFocus = (x.length - 1);
            x[currentFocus].classList.add("autocomplete-active");
        }
        function removeActive(x) {
            for (var i = 0; i < x.length; i++) {
                x[i].classList.remove("autocomplete-active");
            }
        }
        function closeAllLists(elmnt) {
            var x = document.getElementsByClassName("autocomplete-items");
            for (var i = 0; i < x.length; i++) {
                if (elmnt != x[i] && elmnt != inp) {
                    x[i].parentNode.removeChild(x[i]);
                }
            }
        }
        document.addEventListener("click", function (e) {
            closeAllLists(e.target);
        });
    }

    //Can be edited for other useage
    var POL = ["SHEKOU, CN", "YANTIAN, CN", "HONGKONG, HK"];
    var POD = ["LOS ANGELES, CA", "LONG BEACH, CA", "OAKLAND, CA", "SEATTLE, WA", "TACOMA, WA", "VANCOUVER, BC", "PRINCE RUPERT, BC", "NEW YORK, NY", "NOFOLK, VA", "CHARLESTON, SC", "SAVANNAH, GA", "WILMINGTON, NC", "HOUSTON, TX", "MOBILE, AL", "BALTIMORE, MD", "TAMPA, FL", "JACKSONVILLE, FL", "MIAMI, FLBOSTON, MA", "NEW ORLEANS, LA"];
    var FinalDestination = ["CHICAGO, IL", "CINCINNATI, OH", "CLEVELAND, OH", "COLUMBUS, OH", "INDIANAPOLIS, IN", "SAINT PAUL, MN", "MINNEAPOLIS, MN", "DALLAS, TX", "DENVER, CO", "DETROIT, MI", "EL PASO, TX", "KANSAS CITY, KS", "HOUSTON, TX", "NEW ORLEANS, LA", "LOUISVILLE, KY", "NASHVILLE, TN", "MEMPHIS, TN", "SALT LAKE CITY, UT", "SAN ANTONIO, TX", "ST LOUIS, MO", "ATLANTA, GA", "CHARLOTTE, NC", "HARVEY, IL", "GREER, SC", "GEORGETOWN, KY", "HUNTSVILLE, AL", "LAREDO, TX", "PHILADELPHIA, PA", "PITTSBURGH, PA", "PHOENIX, AZ", "PORTLAND, OR"];

    //Target 
    autocomplete(document.getElementById("POL"), POL);
    autocomplete(document.getElementById("POD"), POD);
    autocomplete(document.getElementById("Final_Destination"), FinalDestination);
});