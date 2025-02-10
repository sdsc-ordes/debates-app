<script lang="ts">
  import type { Debate } from "$lib/interfaces/metadata.interface";
  import { displayIsoDate } from "$lib/utils/displayUtils";

  export let debate: Debate;
</script>

<div class="card-title-large" style="color: var(--primary-dark-color);">
  {debate.type}
  {debate.session}
  <div class="date-time-item">
    <!-- <i class="fa fa-calendar" aria-hidden="true"></i> -->
    <div class="card-title-small">{displayIsoDate(debate.schedule)}</div>
  </div>
</div>
