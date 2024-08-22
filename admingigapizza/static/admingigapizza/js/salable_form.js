$(document).ready(function() {
    let editId = null;

    $('#createSalablesModal').on('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const isEdit = button.getAttribute('data-edit');
        const isCreate = button.getAttribute('data-create');

        if (isEdit) {
            editId = button.getAttribute('data-edit');
            salableName = button.getAttribute('data-name');

            salablePrice = button.getAttribute('data-price');
            salablePrice = salablePrice.replace(",", ".");

            salableDescription = button.getAttribute('data-description');
            subcategory = button.getAttribute('data-subcategory');

            $('#createForm').find('input[name="edit_id"]').val(editId);
            $('#createForm').find('input[name="name"]').val(salableName);
            $('#createForm').find('input[name="price"]').val(parseFloat(salablePrice));
            $('#createForm').find('textarea[name="description"]').val(salableDescription);
            $('#createForm').find('select[name="subcategory"]').val(subcategory);
        } else if (isCreate) {
            editId = null;
            
            $('#createForm').find('input[name="edit_id"]').val('');
            $('#createForm').find('input[name="name"]').val('');
            $('#createForm').find('input[name="price"]').val(parseFloat(''));
            $('#createForm').find('textarea[name="description"]').val('');
            $('#createForm').find('select[name="subcategory"]').val('');
        }

        $('#modal-errors').addClass('d-none').html('');
    });

    $('#createForm').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
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