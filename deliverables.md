# ACME Dashboard deliverables (provisional)

**Provenance should be captured at all steps**

**Notification Manager**
* &#x1F534; For all status changes, a notification is created to alert the user of a change.
* &#x1F534; A list of notifications is displayed with all passed steps.
* &#x1F534; The status of all current running jobs is displayed. All status changes go to the notification log.
* &#x1F534; Display of HPC global queue.

**Run Manager**
* &#x1F535; As a user, I should be able to create new run configurations. A run config consists of all the nessisary parameters to start a new run. Runs are broken into five catagories, Model Run, &#x1F534; Create Climatologies, &#x1F534; Archive and transfer, Diagnostic Run, and Publication.
* When runs complete, I should have access to and be able to share run performance information.
* Run configurations and status should be sharable between Dashboard users.
* &#x1F535; As a user, I can browse through all my created run configurations.
* &#x1F535; As a user, I can modify my run configs, &#x1F534; with the ability to undo modifications.
* &#x1F534; As a user with HPC resource access, I should be able to start new Model runs. A model run should give me feedback on its status in real time as the run progresses. When a Model run completes, I should have access to the output files in the Data Manager.
* &#x1F534; As a model is run, every 5 years climatologies are automatially computed and made available to the user. (triggering next step by default)
* &#x1F534; Raw output is copied to HPSS, and climos are transfered to analysis server.(triggering next step by default)
* &#x1F534; Once transfer is complete, diagnostics are computed.(triggering next step by default)
* &#x1F534; Climos published to ESGF after.(triggering next step by default)
* &#x1F534; diag output published to diagnostic viewer.
* &#x1F535; As a user, I should be able to start diagnostic runs on any model or observation data in the Data Manager.


**Data Manager**
* &#x1F534; As a user, I can import a provenance file to recreate mutations on datasets.
* &#x1F534; As a user, I can examine provenance files for all reproducability steps.
* &#x1F535; As a user, I should be able to both upload and download my custom datasets, catagorized as Diagnostic, Model, or Observation. Dataset should be importable from a local computer, a remote server (via URL), or through ESGF.
* &#x1F534; As a user with the ESGF publication role, I should be able to publish any dataset to ESGF.
* &#x1F534; As a user I should be able to create a sharable download link. Download URLs should be created for both individual datafiles as well as entire datasets. These links should be access controlled.
* &#x1F535; As a user, I should be able to browse through my available data.
* &#x1F534; As a user, I should be able to share my data with other Dashboard users.
* &#x1F534; As a user, I should be able to upload my diagnostic output to the diag_viewer, and view it via a link.
* &#x1F534; After a diagnostic is created, I should be able to import to the visualization panel, at the point where I can perform analysis. I should then be able to save as a new plot. Any changes to the plot and share them with other users.
* &#x1F534; As a user, I should be able to specify "favorite" diagnostic plot types which are displayed above others.

**Visualization**
* &#x1F534; As a user, I should be able to import any of my available data into the visualization panel.
* &#x1F534; As a user, I should have the same level of control over visualizations as a UVCDAT user.
* &#x1F534; Once a visualization is created, I should be able to download .png output as well as a script to replicated the visualization locally through UVCDAT.
* &#x1F534; As a user, I should be able to share my visualization configs with other Dashboard users.
