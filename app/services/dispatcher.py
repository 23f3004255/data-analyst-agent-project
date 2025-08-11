from app.tasks import film_analysis, sales_analysis,network_analysis


async def handle_request(questions_file,other_files):
    qtext = (await questions_file.read()).decode("utf-8")
    if "highest grossing films" in qtext.lower():
        return await film_analysis.process(qtext,other_files)
    elif ("sales" in qtext.lower()) or ("revenue" in qtext.lower()):
        return await sales_analysis.process(qtext,other_files)
    elif ("network" in qtext.lower()) or ("edges" in qtext.lower()):
        return await network_analysis.process(qtext,other_files)

    return "unknown file uploaded"

