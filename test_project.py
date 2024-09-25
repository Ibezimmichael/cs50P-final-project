import csv
import pytest
from io import StringIO
import os
from project import is_csv_file, read_individuals_from_csv, create_shift_schedule, generate_pdf, send_email
from unittest.mock import patch, MagicMock, mock_open

def test_is_csv_file():
    assert is_csv_file("valid_file.csv") == True
    assert is_csv_file("invalid_file.txt") == False
    assert is_csv_file("another_file.CSV") == True

def test_read_individuals_from_csv(monkeypatch):
    csv_data = """firstname,lastname,phone,email
John,Doe,1234567890,john@example.com
Jane,Doe,0987654321,jane@example.com
"""
    mock_csv = StringIO(csv_data)
    monkeypatch.setattr('builtins.open', lambda filename, mode: mock_csv)
    individuals = read_individuals_from_csv('mock.csv')
    expected_individuals = [
        {'firstname': 'John', 'lastname': 'Doe', 'phone': '1234567890', 'email': 'john@example.com'},
        {'firstname': 'Jane', 'lastname': 'Doe', 'phone': '0987654321', 'email': 'jane@example.com'}
    ]
    assert individuals == expected_individuals


def test_create_shift_schedule():
    """Test that the generated schedule has exactly 30 days."""
    individuals = [
        {'firstname': 'John', 'lastname': 'Doe', 'email': 'john@example.com', 'phone': '1234567890'},
        {'firstname': 'Jane', 'lastname': 'Smith', 'email': 'jane@example.com', 'phone': '456355'},
        {'firstname': 'Jim', 'lastname': 'Beam', 'email': 'jim@example.com', 'phone': '7893535'}
    ]
    schedule = create_shift_schedule(individuals, num_days=30)
    assert len(schedule) == 30


def test_generate_pdf(tmpdir):
    """Test PDF generation and file creation."""
    individuals = [
        {'firstname': 'John', 'lastname': 'Doe', 'email': 'john@example.com', 'phone': '1234567890'},
        {'firstname': 'Jane', 'lastname': 'Smith', 'email': 'jane@example.com', 'phone': '456355'},
        {'firstname': 'Jim', 'lastname': 'Beam', 'email': 'jim@example.com', 'phone': '7893535'}
    ]
    schedule = create_shift_schedule(individuals, num_days=30)
    pdf_filename = os.path.join(tmpdir, "test_shift_schedule.pdf")
    
    generate_pdf(schedule, pdf_filename)
    assert os.path.isfile(pdf_filename)
    
@pytest.fixture
def email_data():
    """Fixture to provide test data."""
    return {
        'recipient_info': {'email': 'test@example.com'},
        'subject': "Test Email",
        'body': "This is a test email.",
        'attachment': "test.pdf"
    }

def test_send_email_success(email_data):
    """Test successful email sending."""
    with patch('smtplib.SMTP') as mock_smtp:
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value = mock_smtp_instance
        with patch('os.path.isfile') as mock_isfile:
            mock_isfile.return_value = True
            with patch('builtins.open', mock_open(read_data="file data")):
                result = send_email(
                    email_data['recipient_info'],
                    email_data['subject'],
                    email_data['body'],
                    email_data['attachment']
                )
                mock_smtp_instance.sendmail.assert_called_once()
                mock_smtp_instance.login.assert_called_once()
                mock_isfile.assert_called_once_with(email_data['attachment'])
                assert result == True

def test_send_email_file_not_found(email_data):
    """Test email sending with a missing attachment file."""
    with patch('os.path.isfile') as mock_isfile:
        mock_isfile.return_value = False
        result = send_email(
            email_data['recipient_info'],
            email_data['subject'],
            email_data['body'],
            email_data['attachment']
        )
        assert result == False
