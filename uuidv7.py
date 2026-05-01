"""
UUIDv7 생성 모듈

이 모듈은 RFC 9562 규격을 따르는 UUIDv7을 생성합니다.
단, Python 표준 라이브러리인 uuid에서 UUIDv7을 공식적으로 지원할 때까지만
이용하는 것을 가정하고 작성되었습니다.
공식적으로 지원되면 이 모듈의 사용을 자제해주세요.

작성일: 2026-05-01
"""

import time
import os
import uuid


def generate():
    """
    RFC 9562 규격을 따르는 UUIDv7을 생성합니다.
    구조: [48비트 밀리초 시간] + [4비트 버전(7)] + [12비트 난수] + [2비트 배리언트] + [62비트 난수]
    """

    # 1. 현재 시간 (밀리초 단위, 48비트)
    # 2^48 밀리초는 약 서기 10889년까지 표현 가능합니다.
    unix_ts_ms = int(time.time() * 1000)

    # 2. 나머지 80비트를 채울 난수 생성
    rand_bytes = os.urandom(10)
    rand_int = int.from_bytes(rand_bytes, "big")

    # 3. 비트 조립
    # 128비트 UUID 공간 확보 및 시간 데이터 배치
    v7_int = (unix_ts_ms << 80) | (rand_int & 0xFFFFFFFFFFFFFFFFFFFF)

    # 4. 버전 설정 (Version 7: 상위 4비트를 0111로 고정)
    # 128비트 중 80번째 비트부터 4비트 구간
    v7_int &= ~(0xF << 76)  # 해당 구간 초기화
    v7_int |= 0x7 << 76  # 7 주입

    # 5. 배리언트 설정 (Variant 10: 상위 2비트를 10으로 고정)
    # 128비트 중 64번째 비트부터 2비트 구간
    v7_int &= ~(0x3 << 62)  # 해당 구간 초기화
    v7_int |= 0x2 << 62  # 10(2) 주입

    # 6. 표준 UUID 객체로 변환하여 반환
    return uuid.UUID(int=v7_int)


if __name__ == "__main__":
    # 모듈 직접 실행 시 테스트 출력
    new_id = generate()
    print(f"Generated UUIDv7: {new_id}")
    print(f"Hex Format: {new_id.hex}")
