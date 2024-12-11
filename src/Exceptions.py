class TitleLengthError(Exception):
    """DVD 제목 길이 제한 오류"""
    def __init__(self):
        super().__init__("Title length should range from 1 to 30 characters.")

class AuthorLengthError(Exception):
    """감독명 길이 제한 오류"""
    def __init__(self):
        super().__init__("Author length should range from 1 to 20 characters.")

class DuplicateDVDError(Exception):
    """동일 DVD 존재 오류"""
    def __init__(self, title, director):
        super().__init__(f"DVD ({title}, {director}) already exists.")

class UsernameLengthError(Exception):
    """회원명 길이 제한 오류"""
    def __init__(self):
        super().__init__("Username length should range from 1 to 10 characters.")

class DVDNotFoundError(Exception):
    """DVD 부재 오류"""
    def __init__(self, dvd_id):
        super().__init__(f"DVD {dvd_id} does not exist.")

class CannotDeleteBorrowedDVDError(Exception):
    """대출 중인 DVD 삭제 불가 오류"""
    def __init__(self):
        super().__init__("Cannot delete a DVD that is currently borrowed.")

class UserNotFoundError(Exception):
    """회원 부재 오류"""
    def __init__(self, user_id):
        super().__init__(f"User {user_id} does not exist.")

class CannotDeleteBorrowingUserError(Exception):
    """DVD를 대출 중인 회원 삭제 불가 오류"""
    def __init__(self):
        super().__init__("Cannot delete a user with borrowed DVDs.")


class DVDOutOfStockError(Exception):
    """대출 불가능 상태 오류"""
    def __init__(self):
        super().__init__("Cannot check out a DVD that is out of stock.")


class UserBorrowLimitError(Exception):
    """대출 가능 수 제한 오류"""
    def __init__(self, user_id):
        super().__init__(f"User {user_id} exceeded the maximum borrowing limit.")


class RatingRangeError(Exception):
    """영화 평점 범위 제한 오류"""
    def __init__(self):
        super().__init__("Rating should range from 1 to 5 integer value.")


class ReturnAndRateError(Exception):
    """반납 및 평점 미대상 DVD 오류"""
    def __init__(self):
        super().__init__("Cannot return and rate a DVD that is not currently borrowed for this user.")


class DuplicateUserError(Exception):
    """동일한 이름 및 나이의 회원 오류"""
    def __init__(self, name, age):
        super().__init__(f"User ({name}, {age}) already exists.")


class InvalidAgeError(Exception):
    """나이가 양의 정수 값이 아닐 때의 오류"""
    def __init__(self):
        super().__init__("Age should be a positive integer.")


class DuplicateBorrowError(Exception):
    """동일 DVD 여러 번 대출 오류"""
    def __init__(self):
        super().__init__("User cannot borrow same DVD simultaneously.")


class SearchNotFoundError(Exception):
    """검색 실패 시 에러"""
    def __init__(self):
        super().__init__("Cannot find any matching results.")
