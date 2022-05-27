from multiprocessing import context
from pydantic import BaseModel
from typing import Optional

class People(BaseModel):
    """
    작성자 : 장영동
    response 모델
    """
    id : int
    age : int
    workclass : str
    fnlwgt : int
    education : str
    education_num : int
    marital_status : str
    occupation : str
    relationship : str
    race : str
    sex : str
    capital_gain : int
    capital_loss : int
    hours_per_week : int
    native_country : str

    target : int

    class Config:
        orm_mode = True

class Item(BaseModel):
    """
    작성자 : 장영동
    prediction output
    """
    target : int
    context : Optional[str] = None

error_responses =  {
        404 : {
            'description' : 'Additional Response',
             'content' : {
                'application/json' : {
                    'example' : {
                        'exception' : 'Additional Response',
                        'context' : 'API 주소를 확인하세요'
                    }
                }
            }
        },
        200 : {
            'description' : 'Successful Response',
            'content' : {
                'application/json' : {
                    'example' : {
                        'exception': '성공적이라 에러가 없네요',
                        'context' : '아주 참 잘했어요'
                    }
                }
            }
        },
        422 : {
            'description' : 'Validation Error',
            'content' : {
                'application/json' : {
                    'example' : {
                        'exception' : 'Validation Error',
                        'context' : '입력값을 다시 확인해보세요'
                    }
                }
            }
        },
        429 : {
            'description' : 'Time Out Error',
            'content' : {
                'application/json' : {
                    'example' : {
                        'exception' : 'Time Out Error',
                        'context' : 'logging 시간이 많이 걸리네요'
                    }
                }
            }
        },
        500 : {
            'description' : 'Internal Server Error',
            'content' : {
                'application/json' : {
                    'example' : {
                        'exception' : 'Internal Server Error',
                        'context' : '내부 서버 문제입니다'
                    }
                }
            }
        }
    }
