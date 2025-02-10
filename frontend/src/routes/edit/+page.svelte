<script lang="ts">
	import { canEdit } from "$lib/stores/auth";
	import { onMount } from "svelte";
	import { get } from "svelte/store";

	let isEditable: boolean;

	onMount(() => {
		// Set the global edit mode to true when on this page
		canEdit.set(true);

		// Retrieve the current value for debugging or usage
		isEditable = get(canEdit); // Optional, if you need a direct value
	});
</script>

<svelte:head>
	<title>Edit Mode</title>
	<meta name="description" content="Edit mode enabled" />
</svelte:head>

<section>
	<div class="info">
		<div
			class='links'
		>
			<a href="https://github.com/sdsc-ordes/political-debates-ui">
				<i class="fab fa-github"></i>
			</a>
			<a
				href="/"
				class="button-primary-dark"
				style="color: var(--on-primary); text-decoration: none;"
				>Home</a
			>
		</div>
		<div style="display: flex; align-items: center; gap: 0rem;">
			<h1>UNHCR Political Debates</h1>
			<h1 style="color: var(--secondary-color);">/edit</h1>
		</div>

		<div
			style="display: flex; flex-direction: column; justify-content: start; align-items: start; gap: 2rem; width: 100%;"
		>
			<div>
				This is the edit page of the prototype. 
				<br /><br />
				You can now navigate the search and debates pages and make edits
				to the metadata and content. Click on ony debate and edit the speaker name and role. 
				Similarly, you can correct the debate transcriptions and translations per segment. 
				<br /><br />
				Attention! All edits you make to the speakers and
				the text will remain in the database.

				<br /><br />
<!-- 
				Contact us here: TODO EMAIL ADDRESS OR GITHUB?? -->
			</div>
		</div>
		<div class='links'>
			<div>
			<a
				href="/search"
				class="button-highlight"
				style="color: var(--on-primary); text-decoration: none; "
				>Search</a
			>
			</div>
		</div>
	</div>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
		/* border-radius: 20px; */
		/* background-color: var(--primary-color); */
	}

	.links {
		display: flex;
		flex-direction: row;
		justify-content: end;
		width: 100%;
		align-items: end;
		gap: 2rem;
		width: 100%;
	}

	.fa-github {
		font-size: 1.5rem;
		color: var(--primary-dark-color);
	}

	a {
		color: var(--secondary-color);
	}

	h1 {
		font-family: var(--body-font);
		font-size: 36px;
		color: var(--primary-dark-color);
		line-height: 1;
		font-weight: bold;
		padding-top: 3rem;
	}

	.info {
		/* background-color: var(--primary-dark-color); */
		border: 2px dashed var(--primary-dark-color);
		padding: 50px;
		color: var(--text-color);
		margin-top: 1rem;
		border-radius: 10px;
		width: 50%;
		justify-content: start;
		align-items: start;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
</style>
