import setuptools 
  
with open("README.md", "r") as fh: 
    description = fh.read() 
  
setuptools.setup( 
    name="dopple_ai_client", 
    version="1.0.0", 
    author="crimeraaa", 
    author_email="majkelipytania@gmail.com", 
    packages=["dopple_ai_client"], 
    description="Python API wrapper for Dopple.AI", 
    long_description=description, 
    long_description_content_type="text/markdown", 
    url="https://github.com/Crimeraaa-S1GMA/DoppleAIClient", 
    license='MIT', 
    python_requires='>=3.8', 
    install_requires=[] 
) 
