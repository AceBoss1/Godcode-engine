# my-blessing, a newborn scroll.
# Run it with: godcode run main.god
# Test it with: godcode test .

BEGIN CREATION

  DECLARE INTENT "speak a blessing of peace over the household" ON evening_blessing

  DEFINE RITE evening_blessing()
    REVEAL("Peace be upon this house.")
    REVEAL("May the morning bring grace and the evening bring rest.")
  END RITE

  DECLARE day AS "a new day"
  evening_blessing()
  REVEAL("Walk into {day} with courage.")

END CREATION
