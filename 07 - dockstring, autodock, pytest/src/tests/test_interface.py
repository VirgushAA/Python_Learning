import pytest
import inquirer
from interface import start_test, validate_blushing, validate_heart_rate, validate_respiration, validate_pupillary


def test_validate_blushing_raises_exception_not_number():
    """Test that validate_blushing raises a ValidationError when input is not a number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_blushing({}, 'e')


def test_validate_blushing_raises_exception_negative_number():
    """Test that validate_blushing raises a ValidationError when input is a negative number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_blushing({}, '-5')


def test_validate_blushing_raises_exception_bigger_level():
    """Test that validate_blushing raises a ValidationError when input exceeds the maximum level."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_blushing({}, '8')


def test_validate_heart_rate_raises_exception_not_number():
    """Test that validate_heart_rate raises a ValidationError when input is not a number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_heart_rate({}, 'e')


def test_validate_heart_rate_raises_exception_negative_number():
    """Test that validate_heart_rate raises a ValidationError when input is a negative number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_heart_rate({}, '-1')


def test_validate_puppilary_dilation_raises_exception_not_number():
    """Test that validate_pupillary raises a ValidationError when input is not a number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_pupillary({}, 'e')


def test_validate_puppilary_dilation_raises_exception_negative_number():
    """Test that validate_pupillary raises a ValidationError when input is a negative number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_pupillary({}, '-1')


def test_validate_puppilary_dilation_raises_exception_bigger_level():
    """Test that validate_pupillary raises a ValidationError when input exceeds the maximum dilation level."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_pupillary({}, '9')


def test_validate_puppilary_dilation_raises_exception_lower_level():
    """Test that validate_pupillary raises a ValidationError when input is below the minimum dilation level."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_pupillary({}, '1')


def test_validate_respiration_rate_raises_exception_not_number():
    """Test that validate_respiration raises a ValidationError when input is not a number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_respiration({}, 'e')


def test_validate_respiration_rate_raises_exception_negative_number():
    """Test that validate_respiration raises a ValidationError when input is a negative number."""
    with pytest.raises(inquirer.errors.ValidationError):
        validate_respiration({}, '-1')


def test_validate_blushing_valid():
    """Test that validate_blushing returns a valid response for an acceptable input."""
    assert validate_blushing({}, '3')


def test_validate_heart_rate_valid():
    """Test that validate_heart_rate returns a valid response for an acceptable input."""
    assert validate_heart_rate({}, '75')


def test_validate_pupillary_valid():
    """Test that validate_pupillary returns a valid response for an acceptable input."""
    assert validate_pupillary({}, '5')


def test_validate_respiration_valid():
    """Test that validate_respiration returns a valid response for an acceptable input."""
    assert validate_respiration({}, '16')


def test_no_file(capsys):
    """Test that start_test handles a missing file properly and prints an error message."""
    start_test('questions_empty_no_file.json')
    out, err = capsys.readouterr()
    assert out == "File with questions not found.\n"


def test_empty_file(capsys):
    """Test that start_test handles an empty file properly and prints an error message."""
    start_test('tests/questions_invalid/questions_empty.json')  # This should be a 0-byte file
    out, err = capsys.readouterr()
    assert out == "File with questions is empty.\n"


def test_corrupted_file(capsys):
    """Test that start_test handles a corrupted JSON file properly and prints an error message."""
    start_test('tests/questions_invalid/questions_corrupted.json')
    out, err = capsys.readouterr()
    assert out == "File with questions is not valid JSON.\n"
