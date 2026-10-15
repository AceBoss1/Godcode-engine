# Tests for the my-blessing scroll.
# Run them with: godcode test .

BEGIN CREATION

  DEFINE RITE TEST_day_declared()
    DECLARE day AS "a new day"
    TESTIFY day IS "a new day"
  END RITE

  DEFINE RITE TEST_blessing_holds()
    TESTIFY 2 + 3 IS 5
  END RITE

END CREATION
