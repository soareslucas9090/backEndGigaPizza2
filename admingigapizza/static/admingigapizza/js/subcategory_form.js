$(document).ready(function() {
    let editId = null;

    $('#createSubCategoryModal').on('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const isEdit = button.getAttribute('data-edit');
        const isCreate = button.getAttribute('data-create');

        if (isEdit) {
            editId = button.getAttribute('data-edit');
            subcategoryName = button.getAttribute('data-name');
            category = button.getAttribute('data-category');

            $('#createForm').find('input[name="edit_id"]').val(editId);
            $('#createForm').find('input[name="name"]').val(subcategoryName);
            $('#createForm').find('select[name="category"]').val(category);
        } else if (isCreate) {
            editId = null;
            
            $('#createForm').find('input[name="edit_id"]').val('');
            $('#createForm').find('input[name="name"]').val('');
            $('#createForm').find('select[name="category"]').val('');
        }

        $('#modal-errors').addClass('d-none').html('');
    });

    $('#createForm').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                location.reload();
            },
            error: function(xhr) {
                var errors = xhr.responseJSON;
                var errorHtml = '<ul>';
                $.each(errors, function(key, value) {
                    errorHtml += '<li>' + value + '</li>';
                });
                errorHtml += '</ul>';
                $('#modal-errors').html(errorHtml).removeClass('d-none');
            }
        });
    });
});