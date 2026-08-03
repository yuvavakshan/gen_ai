/**
 * script.js
 * ---------
 * Small vanilla-JS helpers that:
 *   1. Populate the "Edit" / "View" / "Delete" modals with data from the
 *      clicked table row (using data-* attributes) before the modal opens.
 *   2. Auto-dismiss flash alerts after a few seconds.
 *
 * No frameworks needed - just the native Bootstrap 5 JS events.
 */

document.addEventListener("DOMContentLoaded", function () {

    // -----------------------------------------------------------------
    // STUDENTS PAGE: Edit Student modal
    // -----------------------------------------------------------------
    const editStudentModal = document.getElementById("editStudentModal");
    if (editStudentModal) {
        editStudentModal.addEventListener("show.bs.modal", function (event) {
            const btn = event.relatedTarget;
            const pk = btn.getAttribute("data-pk");

            document.getElementById("edit_student_id").value = btn.getAttribute("data-id");
            document.getElementById("edit_name").value = btn.getAttribute("data-name");
            document.getElementById("edit_class").value = btn.getAttribute("data-class");
            document.getElementById("edit_email").value = btn.getAttribute("data-email");
            document.getElementById("edit_phone").value = btn.getAttribute("data-phone");

            document.getElementById("editStudentForm").action = "/students/edit/" + pk;
        });
    }

    // STUDENTS PAGE: Delete Student modal
    const deleteStudentModal = document.getElementById("deleteStudentModal");
    if (deleteStudentModal) {
        deleteStudentModal.addEventListener("show.bs.modal", function (event) {
            const btn = event.relatedTarget;
            const pk = btn.getAttribute("data-pk");

            document.getElementById("delete_student_name").textContent = btn.getAttribute("data-name");
            document.getElementById("deleteStudentForm").action = "/students/delete/" + pk;
        });
    }

    // STUDENTS PAGE: View Student Details modal
    const viewStudentModal = document.getElementById("viewStudentModal");
    if (viewStudentModal) {
        viewStudentModal.addEventListener("show.bs.modal", function (event) {
            const btn = event.relatedTarget;

            document.getElementById("view_id").textContent = btn.getAttribute("data-id");
            document.getElementById("view_name").textContent = btn.getAttribute("data-name");
            document.getElementById("view_class").textContent = btn.getAttribute("data-class");
            document.getElementById("view_email").textContent = btn.getAttribute("data-email");
            document.getElementById("view_phone").textContent = btn.getAttribute("data-phone");
            document.getElementById("view_created").textContent = btn.getAttribute("data-created");
        });
    }

    // -----------------------------------------------------------------
    // ATTENDANCE PAGE: Edit Attendance modal
    // -----------------------------------------------------------------
    const editAttendanceModal = document.getElementById("editAttendanceModal");
    if (editAttendanceModal) {
        editAttendanceModal.addEventListener("show.bs.modal", function (event) {
            const btn = event.relatedTarget;
            const pk = btn.getAttribute("data-pk");

            document.getElementById("edit_att_name").textContent = btn.getAttribute("data-name");
            document.getElementById("edit_att_date").textContent = btn.getAttribute("data-date");
            document.getElementById("edit_att_status").value = btn.getAttribute("data-status");
            document.getElementById("edit_att_remarks").value = btn.getAttribute("data-remarks");

            document.getElementById("editAttendanceForm").action = "/attendance/edit/" + pk;
        });
    }

    // ATTENDANCE PAGE: Delete Attendance modal
    const deleteAttendanceModal = document.getElementById("deleteAttendanceModal");
    if (deleteAttendanceModal) {
        deleteAttendanceModal.addEventListener("show.bs.modal", function (event) {
            const btn = event.relatedTarget;
            const pk = btn.getAttribute("data-pk");

            document.getElementById("delete_att_name").textContent = btn.getAttribute("data-name");
            document.getElementById("delete_att_date").textContent = btn.getAttribute("data-date");
            document.getElementById("deleteAttendanceForm").action = "/attendance/delete/" + pk;
        });
    }

    // -----------------------------------------------------------------
    // Auto-dismiss flash alerts after 4 seconds
    // -----------------------------------------------------------------
    document.querySelectorAll(".alert").forEach(function (alertEl) {
        setTimeout(function () {
            const alertInstance = bootstrap.Alert.getOrCreateInstance(alertEl);
            alertInstance.close();
        }, 4000);
    });

});
