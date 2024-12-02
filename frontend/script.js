// Función para cargar la lista de pacientes
function loadPatients() {
    fetch('http://localhost:5000/patients')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Patients List</h2><ul>';
            data.forEach(patient => {
                output += `<li>ID: ${patient.identification_number}, Name: ${patient.name}, Last Name: ${patient.lastname}, Addres: ${patient.address} Phone: ${patient.phone}, Birthdate: ${patient.birthdate}</li>`;
            });
            output += '</ul>';
            document.getElementById('patients').innerHTML = output;
        })
        .catch(err => console.log(err));
}

// Función para agregar un paciente
function addPatient(event) {
    event.preventDefault();

    const idNumber = document.getElementById('patient-id').value;
    const name = document.getElementById('patient-name').value;
    const lastname = document.getElementById('patient-lastname').value;
    const birthdate = document.getElementById('patient-birthdate').value;
    const address = document.getElementById('patient-address').value;
    const phone = document.getElementById('patient-phone').value;

    if (!idNumber || !name || !lastname || !birthdate || !address || !phone) {
        alert("Please fill in all fields.");
        return;
    }

    const patient = {
        identification_number: idNumber,
        name,
        lastname,
        birthdate,
        address,
        phone
    };

    fetch('http://localhost:5000/patients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(patient)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadPatients(); 
    })
    .catch(err => console.log('Error:', err));
}


// Función para cargar la lista de doctores
function loadDoctors() {
    fetch('http://localhost:5000/doctors')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Doctors List</h2><ul>';
            data.forEach(doctor => {
                output += `<li>ID: ${doctor.id_number}, Name: ${doctor.name}, Specialty: ${doctor.specialty}</li>`;
            });
            output += '</ul>';
            document.getElementById('doctors').innerHTML = output;
        })
        .catch(err => console.log(err));
}

// Función para agregar un doctor
function addDoctor(event) {
    event.preventDefault(); 

    const name = document.getElementById('doctor-name').value;
    const specialty = document.getElementById('doctor-specialty').value;
    const phone = document.getElementById('doctor-phone').value;
    const lastname = document.getElementById('doctor-lastname').value;
    const id_number = document.getElementById('doctor-id').value;
    const license = document.getElementById('doctor-license').value;

    if (!name || !lastname || !id_number || !license || !specialty || !phone) {
        alert("Please fill in all fields.");
        return;
    }

    const doctor = { name, lastname, id_number, license, specialty, phone };

    fetch('http://localhost:5000/doctors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(doctor)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        updateDoctorList();
    })
    .catch(err => console.log('Error:', err));
}

/* CITAS */

function loadAppointments() {
    fetch('http://localhost:5000/appointments')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Appointments List</h2><ul>';
            data.forEach(app => {
                output += `<li>ID: ${app.id}, Date: ${app.date}, Time: ${app.time}, Purpose: ${app.purpose}, Status: ${app.status}, Patient: ${app.patient_id}, Doctor: ${app.doctor_id}</li>`;
            });
            output += '</ul>';
            document.getElementById('appointments').innerHTML = output;
        })
        .catch(err => console.log(err));
}

function addAppointment() {
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const purpose = document.getElementById('purpose').value;
    const status = document.getElementById('status').value;
    const patient_id = document.getElementById('patient_id').value;
    const doctor_id = document.getElementById('doctor_id').value;

    fetch('http://localhost:5000/appointments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            date, 
            time,
            purpose,
            status, 
            patient_id, 
            doctor_id 
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadAppointments();
    })
    .catch(err => console.log(err));
}



/* TRATAMIENTOS */

function loadTreatments() {
    fetch('http://localhost:5000/treatments')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Treatments List</h2><ul>';
            data.forEach(treatment => {
                output += `<li>Code: ${treatment.code}, Name: ${treatment.name}, Duration: ${treatment.duration} days, Patient ID: ${treatment.patient_id}, Doctor ID: ${treatment.doctor_id}</li>`;
            });
            output += '</ul>';
            document.getElementById('treatments').innerHTML = output;
        })
        .catch(err => console.log(err));
}


function addTreatment() {
    const code = document.getElementById('treatmentCode').value;
    const name = document.getElementById('treatmentName').value;
    const description = document.getElementById('treatmentDescription').value;
    const duration = document.getElementById('treatmentDuration').value;
    const patientId = document.getElementById('patientId').value;
    const doctorId = document.getElementById('doctorId').value;

    fetch('http://localhost:5000/treatments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code, name, description, duration, patient_id: patientId, doctor_id: doctorId })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadTreatments();
    })
    .catch(err => console.log(err));
}


/* HABITACIONES */

function loadRooms() {
    fetch('http://localhost:5000/rooms')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Rooms List</h2><ul>';
            data.forEach(room => {
                output += `<li>ID:${room.id}, Number:${room.number}, Type: ${room.type}, Capacity: ${room.capacity}, 
                           Available: ${room.available ? 'Yes' : 'No'}</li>`;
            });
            output += '</ul>';
            document.getElementById('rooms').innerHTML = output;
        })
        .catch(err => console.log(err));
}

function addRoom() {
    const number = document.getElementById('roomNumber').value;
    const type = document.getElementById('roomType').value;
    const capacity = document.getElementById('roomCapacity').value;

    if (!number || !type || isNaN(capacity) || capacity <= 0) {
        alert('Please fill all fields correctly.');
        return;
    }

    const validTypes = ["Single", "Shared", "ICU"];
    if (!validTypes.includes(type)) {
        alert('Invalid room type selected.');
        return;
    }

    fetch('http://localhost:5000/rooms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ number, type, capacity, available: true })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadRooms();
    })
    .catch(err => console.log(err));
}

function loadInternments() {
    fetch('http://localhost:5000/internments')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Internments List</h2><ul>';
            data.forEach(internment => {
                output += `<li>Patient ID: ${internment.patient_id}, Room ID: ${internment.room_id}, Admission: ${internment.admission_date}, Discharge: ${internment.discharge_date}</li>`;
            });
            output += '</ul>';
            document.getElementById('internments').innerHTML = output;
        })
        .catch(err => console.log(err));
}

function addInternment() {
    const admission_date = document.getElementById('admissionDate').value;
    const discharge_date = document.getElementById('dischargeDate').value;
    const patient_id = document.getElementById('internmentPatientId').value;
    const room_id = document.getElementById('internmentRoomId').value;

    fetch('http://localhost:5000/internments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ admission_date, discharge_date, patient_id, room_id })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadInternments();
    })
    .catch(err => console.log(err));
}


/* PRESCRIPCIONES */

function loadPrescriptions() {
    fetch('http://localhost:5000/prescriptions')
        .then(response => response.json())
        .then(data => {
            let output = '<h2>Prescriptions List</h2><ul>';
            data.forEach(prescription => {
                output += `<li>Code: ${prescription.code}, Date: ${prescription.date}, Medicine: ${prescription.medicine}, Dose: ${prescription.dose}, Duration: ${prescription.duration}, Patient: ${prescription.patient_id}, Doctor: ${prescription.doctor_id}</li>`;
            });
            output += '</ul>';
            document.getElementById('prescriptions').innerHTML = output;
        })
        .catch(err => console.log(err));
}

function addPrescription() {
    const code = document.getElementById('prescriptionCode').value;
    const date = document.getElementById('prescriptionDate').value;
    const medicine = document.getElementById('medicine').value;
    const dose = document.getElementById('dose').value;
    const duration = document.getElementById('duration').value;
    const patient_id = document.getElementById('prescriptionPatientId').value;
    const doctor_id = document.getElementById('prescriptionDoctorId').value;

    fetch('http://localhost:5000/prescriptions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, date, medicine, dose, duration, patient_id, doctor_id })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadPrescriptions();
    })
    .catch(err => console.log(err));
}


