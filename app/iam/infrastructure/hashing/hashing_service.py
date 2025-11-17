"""
Hashing Service for hashing passwords of the users.
"""
import bcrypt

class HashingService:
    """
    Service for hashing and verifying passwords using bcrypt.
    
    Bcrypt has a maximum password length of 72 bytes. Passwords longer
    than this are automatically truncated to comply with this limit.
    """
    
    # Bcrypt has a maximum password length of 72 bytes
    MAX_PASSWORD_LENGTH = 72
    
    @staticmethod
    def hash(password: str) -> str:
        """
        Hashes a password using bcrypt.
        
        Bcrypt has a 72-byte limit. If the password is longer, it will be
        automatically truncated to prevent errors.

        :param password: The password to be hashed
        :return: The hashed password
        """
        # Truncate password to 72 bytes if necessary (bcrypt limitation)
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > HashingService.MAX_PASSWORD_LENGTH:
            password_bytes = password_bytes[:HashingService.MAX_PASSWORD_LENGTH]
        
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Compares a plain password with a hashed password.
        
        The plain password is truncated to 72 bytes before verification
        to match the behavior during hashing.

        :param plain_password: A plain password to be compared
        :param hashed_password: The hashed password to be compared
        :return: True if the passwords match, False otherwise
        """
        # Truncate password to 72 bytes if necessary (bcrypt limitation)
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > HashingService.MAX_PASSWORD_LENGTH:
            password_bytes = password_bytes[:HashingService.MAX_PASSWORD_LENGTH]
        
        # Compare passwords
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)