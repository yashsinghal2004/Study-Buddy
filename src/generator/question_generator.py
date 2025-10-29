#most imp file
from langchain.output_parsers import PydanticOutputParser #llm output converted to struc output
from src.models.question_schemas import MCQQuestion, FillInTheBlankQuestion #datamodels for defining struc for both
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.llm.groq_client import get_groq_client #calling the llm
from src.config.settings import settings 
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    def __init__(self):#constructor
        self.llm=get_groq_client() #our llm will be put into use instantly
        self.logger=get_logger(self.__class__.__name__)

        # helper function- go in llm parse the message and see if sm wrong or not
    def _retry_and_parser(self,prompt,parser,topic,difficulty):

        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")

                response = self.llm.invoke(prompt.format(topic=topic,difficulty=difficulty))

                parsed=parser.parse(response.content)

                self.logger.info("Successfully parsed the question")

                return parsed

            except Exception as e:
                self.logger.error(f"Error coming : {str(e)}")
                if attempt==settings.MAX_RETRIES-1:
                    raise  CustomException(f"Generation failed after {settings.MAX_RETRIES} attempts",e)  

    
    
    def generate_mcq(self,topic:str,difficulty:str='medium')->MCQQuestion:# this will follow the pattern of mcqquestion schema
        try: 
            parser=PydanticOutputParser(pydantic_object=MCQQuestion)# initialised parser with question schema

            question=self._retry_and_parser(mcq_prompt_template,parser,topic,difficulty)# que is genrated

            #extra check 
            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure") # or customexception error

            self.logger.info("Generating a valid MCQ QUestion")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ : {str(e)}")
            raise CustomException("MCQ Generation Failed",e)    



    def generate_fill_blank(self,topic:str,difficulty:str='medium')->FillInTheBlankQuestion:# this will follow the pattern of fillblank schema
        try: 
            parser=PydanticOutputParser(pydantic_object=FillInTheBlankQuestion)# initialised parser with question schema

            question=self._retry_and_parser(fill_blank_prompt_template,parser,topic,difficulty)# que is genrated

            #extra check
            if "___" not in question.question:
                raise ValueError("Fill in the blank should contain '___'")
            
            self.logger.info("Generating a valid Fill in the blank QUestion")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate fillups  : {str(e)}")
            raise CustomException("Fill in blank generation failed",e) 



