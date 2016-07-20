* NOTE *
For the purposes of this document, all "user_id" is the id created from the web_fe database. The id created from 
Pegasus will be refered to as the "run_user_id"

/update
    - All jobs
      GET:   
      - params: {"request": “all”, "user": user_id }
         no user -> respond with status of all jobs
         user    -> respond with status of all jobs for the given user
      POST: 
      - params: {"request": “all”, "user": user_id, "requested_staus": status }
          requested_status: {pause, start, stop}
          no user -> change status of all jobs
          user      -> change status of all jobs for given user
          
    - Next
      GET
      - params: {"request": "next"}
        responds with the next job on the queue and changes that jobs status to "in_progress"

    - New Jobs
      GET: 
      - params: {"request": “new”, "user": user_id }
         no user -> respond with all new jobs
         user    -> respond with all jobs for given user
 
      POST: 
      - params: {"request": “new”, "user": user_id, "config_options": {"some:"options"}  }
        config_options: A JSON encoded object holding run configuration options
        user_id: the user id
        -> creates new job for user with given config options

    - In progress
      GET: 
      - params: {"request": “in_progress”, "user": user_id }
          no user -> respond with all in_progress jobs
          user    -> respond with all in_progress jobs for given user
      POST:
      - params: {"request": “in_progress”, "user": user_id, "job_id": job_id }
          job_id  -> updates job status to “in_progress”

    - Complete
      GET: 
      - params: {"request": “complete”, "user": user_id }
        no user -> respond with all complete jobs
        user    -> respond with all complete jobs for given user
        
      POST:
      - params: {"request": “complete”, "user": user_id, "job_id": job_id }
        job_id  -> updates job status to “complete”

    - Job
      GET: 
      - params: {"request": “job”, "job_id": job_id }
        job_id  -> respond with current job status
      
    - Run_user_id
      POST:
      - params: {"request": “run_id”, "user": user_id, "run_user_id": run_user_id }
        run_user_id  -> The user id created by Pegasus


