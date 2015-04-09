S3 Bucket Deleter
=================

We had an unfortunately too-large-to-list bucket. No existing tools could
list the full contents or generate a full usage list, and it was deemed that this
bucket was expendable. So I set about using the task of deleting this content
as an example deployment to the new [Deis](http://deis.io/) cluster.

HOWTO
=====

    git clone git@github.com:jcderr/deis-clear-s3-bucket.git
    cd deis-clear-s3-bucket
    deis register http://[deis hostname]/
       ...
    deis create clear-s3-bucket
    deis config:set AWS_ACCESS_KEY_ID=[ ... ]
    deis config:set AWS_SECRET_ACCESS_KEY=[ ... ]
    deis config:set BUCKET=[ ... ]
        [ Optionally also set INITIAL_WAIT to give the list filler more time ]
    git push deis master
    
After some time, you can see the output by running `deis logs`.
