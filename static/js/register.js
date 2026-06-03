let selectedType = "";
let selectedOrgType = "";

function selectAccount(type){

selectedType = type;

if(type === "Individual"){

    document.getElementById("step1").style.display = "none";
    document.getElementById("individualForm").style.display = "block";

}else{

    document.getElementById("step1").style.display = "none";
    document.getElementById("step2").style.display = "block";

}

}

function selectOrgType(type){

selectedOrgType = type;

document.getElementById("step2").style.display = "none";
document.getElementById("step3").style.display = "block";

loadDynamicFields(type);

}

function loadDynamicFields(type){

const container =
document.getElementById("dynamicFields");

let html = "";

if(type === "Hospital"){

    html = `
    <input id="registration_number"
    placeholder="Hospital Registration Number">

    <input id="buildings"
    placeholder="Number of Buildings">

    <input id="beds"
    placeholder="Number of Beds">

    <input id="departments"
    placeholder="Number of Departments">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "Apartment"){

    html = `
    <input id="registration_number"
    placeholder="Association Registration Number">

    <input id="towers"
    placeholder="Number of Towers">

    <input id="flats"
    placeholder="Number of Flats">

    <input id="security_staff"
    placeholder="Security Staff Count">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "College"){

    html = `
    <input id="registration_number"
    placeholder="Institution Registration Number">

    <input id="students"
    placeholder="Number of Students">

    <input id="faculty"
    placeholder="Faculty Count">

    <input id="campuses"
    placeholder="Number of Campuses">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "School"){

    html = `
    <input id="registration_number"
    placeholder="School Registration Number">

    <input id="students"
    placeholder="Number of Students">

    <input id="teachers"
    placeholder="Teacher Count">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "IT Company"){

    html = `
    <input id="registration_number"
    placeholder="Company Registration Number">

    <input id="website"
    placeholder="Company Website">

    <input id="campuses"
    placeholder="Number of Campuses">

    <input id="facility_team"
    placeholder="Facility Team Size">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "MNC"){

    html = `
    <input id="registration_number"
    placeholder="Corporate Registration Number">

    <input id="website"
    placeholder="Corporate Website">

    <input id="global_locations"
    placeholder="Global Locations">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "Warehouse"){

    html = `
    <input id="registration_number"
    placeholder="Warehouse Registration Number">

    <input id="capacity"
    placeholder="Storage Capacity">

    <input id="loading_bays"
    placeholder="Loading Bays">

    <input id="shifts"
    placeholder="Number of Shifts">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else if(type === "Industry"){

    html = `
    <input id="registration_number"
    placeholder="Factory License Number">

    <input id="plant_area"
    placeholder="Plant Area">

    <input id="production_lines"
    placeholder="Production Lines">

    <input id="employee_count"
    placeholder="Employee Count">
    `;

}

else{

    html = `
    <input id="employee_count"
    placeholder="Employee Count">
    `;
}

container.innerHTML = html;

}

function nextOwner(){

document.getElementById("step3").style.display = "none";
document.getElementById("step4").style.display = "block";

}

async function registerIndividual(){

const data = {

    full_name:
    document.getElementById("full_name").value,

    email:
    document.getElementById("email").value,

    mobile:
    document.getElementById("mobile").value,

    password:
    document.getElementById("individual_password").value
};

const response = await fetch(
"/register/individual",
{
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body:JSON.stringify(data)
});

const result = await response.json();

alert(result.message);

}

async function registerOrganization(){

if(
document.getElementById("password").value !==
document.getElementById("confirm_password").value
){

    alert("Passwords do not match");
    return;
}

let extraData = {};

if(selectedOrgType === "Hospital"){

    extraData = {

        registration_number:
        document.getElementById("registration_number").value,

        buildings:
        document.getElementById("buildings").value,

        beds:
        document.getElementById("beds").value,

        departments:
        document.getElementById("departments").value
    };
}

else if(selectedOrgType === "Apartment"){

    extraData = {

        registration_number:
        document.getElementById("registration_number").value,

        towers:
        document.getElementById("towers").value,

        flats:
        document.getElementById("flats").value,

        security_staff:
        document.getElementById("security_staff").value
    };
}

const employeeField =
document.getElementById("employee_count");

const data = {

    organization_name:
    document.getElementById("org_name").value,

    organization_type:
    selectedOrgType,

    official_email:
    document.getElementById("official_email").value,

    official_mobile:
    document.getElementById("official_mobile").value,

    country:
    document.getElementById("country").value,

    state:
    document.getElementById("state").value,

    city:
    document.getElementById("city").value,

    address:
    document.getElementById("address").value,

    employee_count:
    employeeField
    ? parseInt(employeeField.value || 0)
    : 0,

    owner_name:
    document.getElementById("owner_name").value,

    designation:
    document.getElementById("designation").value,

    owner_email:
    document.getElementById("owner_email").value,

    owner_mobile:
    document.getElementById("owner_mobile").value,

    password:
    document.getElementById("password").value,

    extra_data:
    JSON.stringify(extraData)
};

const response = await fetch(
"/register/organization",
{
    method:"POST",
    headers:{
        "Content-Type":"application/json"
    },
    body:JSON.stringify(data)
});

const result = await response.json();

if(result.organization_id){

    alert(
    "Organization Registered Successfully\n\nOrganization ID: " +
    result.organization_id
    );

    window.location.href =
    "/login-page";

}else{

    alert(
    result.detail ||
    "Registration Failed"
    );
}

}