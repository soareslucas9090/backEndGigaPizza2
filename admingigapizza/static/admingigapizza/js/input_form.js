$(document).ready(function() {
    let editId = null;

    $('#createInputsModal').on('show.bs.modal', function(event) {
        const button = event.relatedTarget;
        const isEdit = button.getAttribute('data-edit');
        const isCreate = button.getAttribute('data-create');

        if (isEdit) {
            editId = button.getAttribute('data-edit');
            inputName = button.getAttribute('data-name');

            inputPrice = button.getAttribute('data-price');
            inputPrice = inputPrice.replace(",", ".")

            inputUnit = button.getAttribute('data-unit');

            inputQuantity = button.getAttribute('data-quantity');
            inputQuantity = inputQuantity.replace(",", ".")

            subcategory = button.getAttribute('data-subcategory');

            $('#createForm').find('input[name="edit_id"]').val(editId);
            $('#createForm').find('input[name="name"]').val(inputName);
            $('#createForm').find('input[name="quantity"]').val(parseFloat(inputQuantity));
            $('#createForm').find('input[name="price"]').val(parseFloat(inputPrice));
            $('#createForm').find('select[name="unit"]').val(inputUnit);
            $('#createForm').find('select[name="subcategory"]').val(subcategory);
        } else if (isCreate) {
            editId = null;
            
            $('#createForm').find('input[name="edit_id"]').val('');
            $('#createForm').find('input[name="name"]').val('');
            $('#createForm').find('input[name="price"]').val('');
            $('#createForm').find('input[name="unit"]').val('');
            $('#createForm').find('input[name="quantity"]').val('');
            $('#createForm').find('select[name="subcategory"]').val('');
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